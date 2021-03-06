from phpserialize.errors import PhpUnserializationError, PhpSerializationError, \
    _PhpUnserializationError


class PHP_Class(object):
    def __init__(self, name, properties=()):
        self.name = name
        self._properties = {}
        for prop in properties:
            self._properties[prop.name] = prop

    def set_item(self, php_name, value=None):
        prop = PHP_Property(php_name, value)
        self._properties[prop.name] = prop

    def __iter__(self):
        return iter(self._properties.values())

    def __len__(self):
        return len(self._properties)

    def __repr__(self):
        return "PHP_Class(%s, %s)" % (repr(self.name), list(self))

    __unicode__ = __str__ = __repr__

    def __getitem__(self, name):
        return self._properties[name].value

    def __eq__(self, other):
        return repr(self) == repr(other)


class PHP_Property(object):
    SEPARATOR = '\x00'
    def __init__(self, php_name, value):
        self.php_name = php_name
        self.name = php_name.split(self.SEPARATOR)[-1]
        self.value = value

    def __repr__(self):
        return 'PHP_Property(%s, %s)' % (repr(self.php_name), repr(self.value))

    __str__ = __unicode__ = __repr__


def unserialize(s):
    """
    Unserialize python struct from php serialization format
    """
    if not isinstance(s, basestring):
        raise ValueError('Unserialize argument must be string')
    try:
        return Unserializator(s).unserialize()
    except _PhpUnserializationError, e:
        char = len(str(s)) - len(e.rest)
        delta = 50
        try:
            sample = '...%s --> %s <-- %s...' % (
                s[(char > delta and char - delta or 0):char],
                s[char],
                s[char + 1:char + delta]
            )
            message = '%s in %s' % (e.message, sample)
        except Exception, e:
            raise
        raise PhpUnserializationError(message)

def serialize(struct):
    """
    Serialize python struct into php serialization format
    """
    # N;
    if struct is None:
        return 'N;'

    struct_type = type(struct)
    # d:<float>;
    if struct_type is float:
        return 'd:%.20f;' % struct  # 20 digits after comma

    # b:<0 or 1>;
    if struct_type is bool:
        return 'b:%d;' % int(struct)

    # i:<integer>;
    if struct_type is int or struct_type is long:
        return 'i:%d;' % struct

    # s:<string_length>:"<string>";
    if struct_type is str:
        return 's:%d:"%s";' % (len(struct), struct)

    if struct_type is unicode:
        return serialize(struct.encode('utf-8'))

    # a:<hash_length>:{<key><value><key2><value2>...<keyN><valueN>}
    if struct_type is dict:
        core = ''.join([serialize(k) + serialize(v) for k, v in struct.items()])
        return 'a:%d:{%s}' % (len(struct), core)

    if struct_type is tuple or struct_type is list:
        return serialize(dict(enumerate(struct)))

    if isinstance(struct, PHP_Class):
        return 'O:%d:"%s":%d:{%s}' % (
            len(struct.name),
            struct.name,
            len(struct),
            ''.join([serialize(x.php_name) + serialize(x.value) for x in struct]),
        )

    raise PhpSerializationError('PHP serialize: cannot encode `%s`' % struct)


class Unserializator(object):
    def __init__(self, s):
        self._position = 0
        self._str = s

    def await(self, symbol, n=1):
        #result = self.take(len(symbol))
        result = self._str[self._position:self._position + n]
        self._position += n
        if result != symbol:
            raise _PhpUnserializationError('Next is `%s` not `%s`' % (result, symbol), self.get_rest())

    def take(self, n=1):
        result = self._str[self._position:self._position + n]
        self._position += n
        return result

    def take_while_not(self, stopsymbol, typecast=None):
        try:
            stopsymbol_position = self._str.index(stopsymbol, self._position)
        except ValueError:
            raise _PhpUnserializationError('No `%s`' % stopsymbol, self.get_rest())
        result = self._str[self._position:stopsymbol_position]
        self._position = stopsymbol_position + 1
        if typecast is None:
            return result
        else:
            return typecast(result)

    def get_rest(self):
        return self._str[self._position:]

    def unserialize(self):
        t = self.take()

        if t == 'N':
            self.await(';')
            return None

        self.await(':')

        if t == 'i':
            return self.take_while_not(';', int)

        if t == 'd':
            return self.take_while_not(';', float)

        if t == 'b':
            return bool(self.take_while_not(';', int))

        if t == 's':
            size = self.take_while_not(':', int)
            self.await('"')
            result = self.take(size)
            self.await('";', 2)
            return result

        if t == 'a':
            size = self.take_while_not(':', int)
            return self.parse_hash_core(size)

        if t == 'O':
            object_name_size = self.take_while_not(':', int)
            self.await('"')
            object_name = self.take(object_name_size)
            self.await('":', 2)
            object_length = self.take_while_not(':', int)
            php_class = PHP_Class(object_name)
            members = self.parse_hash_core(object_length)
            if members:
                for php_name, value in members.items():
                    php_class.set_item(php_name, value)
            return php_class

        raise _PhpUnserializationError('Unknown type `%s`' % t, self.get_rest())

    def parse_hash_core(self, size):
        result = {}
        self.await('{')
        is_array = True
        for i in range(size):
            k = self.unserialize()
            v = self.unserialize()
            result[k] = v
            if is_array and k != i:
                is_array = False
        if is_array:
            result = result.values()
        self.await('}')
        return result

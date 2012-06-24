from pypy.rlib.objectmodel import newlist_hint, compute_hash
from pypy.rlib.rarithmetic import intmask
from pypy.rlib.rerased import new_static_erasing_pair

from rupypy.module import ClassDef
from rupypy.modules.comparable import Comparable
from rupypy.objects.objectobject import W_Object
from rupypy.objects.rangeobject import W_RangeObject
from rupypy.objects.intobject import W_FixnumObject


class StringStrategy(object):
    def __init__(self, space):
        pass


class ConstantStringStrategy(StringStrategy):
    erase, unerase = new_static_erasing_pair("constant")

    def str_w(self, storage):
        return self.unerase(storage)

    def liststr_w(self, storage):
        strvalue = self.unerase(storage)
        return [c for c in strvalue]

    def length(self, storage):
        return len(self.unerase(storage))

    def hash(self, storage):
        return compute_hash(self.unerase(storage))

    def copy(self, space, storage):
        return W_StringObject(space, storage, self)

    def to_mutable(self, space, s):
        s.strategy = strategy = space.fromcache(MutableStringStrategy)
        s.str_storage = strategy.erase(self.liststr_w(s.str_storage))

    def extend_into(self, src_storage, dst_storage):
        dst_storage += self.unerase(src_storage)


class MutableStringStrategy(StringStrategy):
    erase, unerase = new_static_erasing_pair("mutable")

    def str_w(self, storage):
        return "".join(self.unerase(storage))

    def liststr_w(self, storage):
        return self.unerase(storage)

    def length(self, storage):
        return len(self.unerase(storage))

    def hash(self, storage):
        storage = self.unerase(storage)
        length = len(storage)
        if length == 0:
            return -1
        x = ord(storage[0]) << 7
        i = 0
        while i < length:
            x = intmask((1000003 * x) ^ ord(storage[i]))
            i += 1
        x ^= length
        return intmask(x)

    def to_mutable(self, space, s):
        pass

    def extend_into(self, src_storage, dst_storage):
        dst_storage += self.unerase(src_storage)

    def clear(self, s):
        self.unerase(s.str_storage)[:] = []


class W_StringObject(W_Object):
    classdef = ClassDef("String", W_Object.classdef)
    classdef.include_module(Comparable)

    def __init__(self, space, storage, strategy):
        W_Object.__init__(self, space)
        self.str_storage = storage
        self.strategy = strategy

    @staticmethod
    def newstr_fromstr(space, strvalue):
        strategy = space.fromcache(ConstantStringStrategy)
        storage = strategy.erase(strvalue)
        return W_StringObject(space, storage, strategy)

    @staticmethod
    def newstr_fromchars(space, chars):
        strategy = space.fromcache(MutableStringStrategy)
        storage = strategy.erase(chars)
        return W_StringObject(space, storage, strategy)

    def str_w(self, space):
        return self.strategy.str_w(self.str_storage)

    def liststr_w(self, space):
        return self.strategy.liststr_w(self.str_storage)

    def length(self):
        return self.strategy.length(self.str_storage)

    def copy(self, space):
        return self.strategy.copy(space, self.str_storage)

    def extend(self, space, w_other):
        self.strategy.to_mutable(space, self)
        strategy = self.strategy
        assert isinstance(strategy, MutableStringStrategy)
        storage = strategy.unerase(self.str_storage)
        w_other.strategy.extend_into(w_other.str_storage, storage)

    @classdef.method("to_s")
    def method_to_s(self, space):
        return self

    @classdef.method("+")
    def method_plus(self, space, w_other):
        assert isinstance(w_other, W_StringObject)
        total_size = self.length() + w_other.length()
        s = space.newstr_fromchars(newlist_hint(total_size))
        s.extend(space, self)
        s.extend(space, w_other)
        return s

    @classdef.method("<<")
    def method_lshift(self, space, w_other):
        assert isinstance(w_other, W_StringObject)
        self.extend(space, w_other)
        return self

    @classdef.method("length")
    def method_length(self, space):
        return space.newint(self.length())

    @classdef.method("hash")
    def method_hash(self, space):
        return space.newint(self.strategy.hash(self.str_storage))

    @classdef.method("<=>")
    def method_comparator(self, space, w_other):
        assert isinstance(w_other, W_StringObject)
        s1 = space.str_w(self)
        s2 = space.str_w(w_other)
        if s1 < s2:
            return space.newint(-1)
        elif s1 == s2:
            return space.newint(0)
        elif s1 > s2:
            return space.newint(1)

    @classdef.method("freeze")
    def method_freeze(self, space):
        pass

    @classdef.method("to_sym")
    @classdef.method("intern")
    def method_to_sym(self, space):
        return space.newsymbol(space.str_w(self))

    @classdef.method("clear")
    def method_clear(self, space):
        self.strategy.to_mutable(space, self)
        self.strategy.clear(self)
        return self

    @classdef.method("[]")
    def method_subscript(self, space, w_idx):
        length = self.length()
        if isinstance(w_idx, W_RangeObject):
            start = space.int_w(w_idx.w_start)
            
            if start > length or start < -length:
                return space.w_nil
            
            if w_idx.exclusive:
                end = space.int_w(w_idx.w_end)
            else:
                end = space.int_w(w_idx.w_end) + 1
            
            if start < 0:
                if end > 0:
                    return space.newstr_fromstr("")
                start = length + start
            if end <= 0:
                end = length + end
            
            return space.newstr_fromstr(space.str_w(self)[start:end])
        else:
            assert isinstance(w_idx, W_FixnumObject)
            index = space.int_w(w_idx)
            if index >= length or index < -length:
                return space.w_nil
            return space.newstr_fromstr(space.str_w(self)[index])

    @classdef.method("next")
    @classdef.method("succ")
    def method_succ(self, space):
        # NOT COMPLETE
        s1 = space.str_w(self)[-1]
        s2 = chr(ord(s1) + 1)
        return space.newstr_fromstr(s2)

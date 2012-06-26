from rupypy.module import ClassDef
from rupypy.modules.enumerable import Enumerable
from rupypy.objects.objectobject import W_Object
from rupypy.objects.intobject import W_FixnumObject


class W_RangeObject(W_Object):
    classdef = ClassDef("Range", W_Object.classdef)
    classdef.include_module(Enumerable)

    def __init__(self, space, w_start, w_end, exclusive = False):
        W_Object.__init__(self, space)

        self.w_start = w_start
        self.w_end = w_end
        self.exclusive = exclusive

    @classdef.singleton_method("allocate")
    def method_allocate(self, space):
        return W_RangeObject(space, space.w_nil, space.w_nil)

    @classdef.singleton_method("new")
    def method_new(self, space, w_start, w_end, w_exclusive = None):
        if w_exclusive is None:
            w_exclusive = space.newbool(False)
        exclusive = w_exclusive.is_true(space)
        return W_RangeObject(space, w_start, w_end, exclusive)

    @classdef.method("begin")
    def method_begin(self, space):
        return self.w_start

    @classdef.method("end")
    def method_end(self, space):
        return self.w_end

    @classdef.method("exclude_end?")
    def method_exclude_end(self, space):
        return space.newbool(self.exclusive)

    classdef.app_method("""
    def ==(other)
        if other.instance_of? Range
            if self.begin == other.begin && self.end == other.end
                if self.exclude_end? == other.exclude_end?
                    return true
                end
            end
        end
        false
    end

    def ===(other)
        include? other
    end

    def member?(other)
        include? other
    end

    def include?(other)
        if other.is_a? Fixnum
            return cover? other
        end
        
        if self.begin.is_a?(String) && self.begin.length == 1
            if self.end.is_a?(String) && self.end.length == 1
                if other.is_a?(String) && other.length == 1
                    if self.begin.ord <= other.ord
                        if self.exclude_end?
                            if other.ord < self.end.ord
                                return true
                            end
                        else
                            if other.ord <= self.end.ord
                                return true
                            end
                        end
                    end
                end
            end
        end
        
        self.each do |i|
            return true if i == other
        end
        false
    end

    def cover?(other)
        if self.begin <= other
            if self.exclude_end?
                if other < self.end
                    return true
                end
            else
                if other <= self.end
                    return true
                end
            end
        end
        false
    end

    def each
        i = self.begin
        lim = self.end
        if !self.exclude_end?
            lim = lim.succ
        end
        while i < lim
            yield i
            i = i.succ
        end
    end

    def to_a
        x = []
        self.each do |elem|
            x << elem
        end
        x
    end
    """)

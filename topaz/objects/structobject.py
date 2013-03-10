# First implementation using hash
# Second implementation using a map with jit annotations

from topaz.objects.objectobject import W_Object
from topaz.objects.stringobject import W_StringObject
from topaz.objects.symbolobject import W_SymbolObject
from topaz.module import ClassDef
from topaz.modules.enumerable import Enumerable


class W_StructObject(W_Object):
    classdef = ClassDef("Struct", W_Object.classdef, filepath=__file__)
    classdef.include_module(Enumerable)

    def __init__(self, space, w_args):
        print "__init__", w_args
        self.attributes = {}
        for attribute_w in w_args:
            if not isinstance(attribute_w, W_StringObject) and not isinstance(attribute_w, W_SymbolObject):
                raise space.error(space.w_TypeError, "%s is not a symbol" % space.str_w(attribute_w))
            self.attributes[space.str_w(attribute_w)] = None

    # Struct.new("Foo") #=> Struct::Foo
    # Struct.new(:a, :b) #=> <#Class:0x00>
    @classdef.singleton_method("new")
    def singleton_method_new(self, space, args_w, block):
        print "singleton new"
        if len(args_w) == 0:
            raise space.error(space.w_ArgumentError, "wrong number of arguments (0 for 1+)")

        if isinstance(args_w[0], W_StringObject):
            # build class with supplied symbols as attributes and assign it to
            # the given name as a constant
            w_struct = W_StructObject(space, args_w[1:])
            w_cls = space.newclass("Struct::Foo", w_struct, True)

            # add attributes and stuff

            name = space.str_w(args_w[0])
            space.set_const(space.w_struct, name, w_cls)
            return w_cls
        else:
            return W_StructObject(space, args_w)
        #return space.newclass("", self)

    @classdef.singleton_method("allocate")  # Struct.allocate
    def singleton_method_allocate(self, space):
        print "singleton_method_allocate"
        raise space.error(space.w_TypeError, "allocator undefined for Struct")

    @classdef.method("new")  # Struct.new #=> <#Class:0x00>
    def method_new(self, space, args_w, block):
        print "method_new"

    @classdef.method("allocate")  # Struct.new.allocate # should be class?
    def method_allocate(self, space):
        print "method_allocate"

    @classdef.method("initialize")  # Struct.new.new #=> <#struct x=nil>
    def method_initialize(self, space, w_args):
        # w_args holds values for the previous defined keys!
        # question: where to get the keys from??
        print "method_initialize", w_args

        # print "keys", self.attributes.keys()

        #self.attributes = {}
        #for attribute_w in w_args:
        #    self.attributes[space.str_w(attribute_w)] = None

    def inherited(self, space, w_mod):
        pass
        #self.descendants.append(w_mod)
        #if not space.bootstrap and space.respond_to(self, space.newsymbol("inherited")):
        #    space.send(self, space.newsymbol("inherited"), [w_mod])

    def str_w(self, space):
        token = ["<#struct"]
        for key, value in self.attributes.iteritems():
            token.append("%s=%s" % (key, value))
        return " ".join(token) + ">"

    @classdef.method("size")
    @classdef.method("length")
    def method_length(self, space):
        return space.newint(len(self.attributes))

    @classdef.method("members")
    def method_members(self, space):
        # TODO: check for keys being symbols
        return space.newarray(self.attributes.keys())

    @classdef.method("to_a")
    @classdef.method("values")
    def method_values(self, space):
        return space.newarray(self.attributes.values())

    @classdef.method("inspect")
    @classdef.method("to_s")
    def method_to_s(self, space):
        return space.newstr_fromstr(self.str_w(space))

    @classdef.method("to_h")
    def method_to_h(self, space):
        w_hash = space.newhash()
        for key, value in self.attributes.iteritems():
            w_hash.method_subscript_assign(key, value)
        return w_hash

    #@classdef.method("values_at")
    #def method_values_at(self, space, w_args):
    #    w_values = space.newarray([])
    #    values = self.attributes.values()
    #    for w_idx in w_args:
    #        idx = space.w_int(w_idx)
    #        w_values.method_append(space, values[idx])
    #    return w_values

    @classdef.method("method_missing")
    def method_method_missing(self, space, w_name, args_w):
        if len(args_w) == 0:  # Getter
            self.attributes[space.str_w]

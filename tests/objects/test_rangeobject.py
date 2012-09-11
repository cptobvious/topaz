from ..base import BaseRuPyPyTest


class TestRangeObject(BaseRuPyPyTest):
    def test_map(self, space):
        w_res = space.execute("return (1..3).map {|x| x * 5}")
        assert self.unwrap(space, w_res) == [5, 10, 15]

        w_res = space.execute("return (1...3).map {|x| x * 5}")
        assert self.unwrap(space, w_res) == [5, 10]

    def test_starting_point_always_returned(self, space):
        w_res = space.execute("return (1..1).map {|x| x}")
        assert self.unwrap(space, w_res) == [1]

    def test_alphanumeric_values(self, space):
        w_res = space.execute("return ('a'..'e').to_a")
        assert self.unwrap(space, w_res) == ['a', 'b', 'c', 'd', 'e']

    def test_to_a(self, space):
        w_res = space.execute("return (1..3).to_a")
        assert self.unwrap(space, w_res) == [1, 2, 3]

        w_res = space.execute("return (1...3).to_a")
        assert self.unwrap(space, w_res) == [1, 2]

        w_res = space.execute("return (3..2).to_a")
        assert self.unwrap(space, w_res) == []

    def test_begin(self, space):
        w_res = space.execute("return (5..10).begin")
        assert self.unwrap(space, w_res) == 5

        w_res = space.execute("return ('1'..'5').begin")
        assert self.unwrap(space, w_res) == "1"

    def test_end(self, space):
        w_res = space.execute("return (5..10).end")
        assert self.unwrap(space, w_res) == 10

        w_res = space.execute("return (5...10).end")
        assert self.unwrap(space, w_res) == 10

        w_res = space.execute("return ('1'..'5').end")
        assert self.unwrap(space, w_res) == "5"

        w_res = space.execute("return ('1'...'5').end")
        assert self.unwrap(space, w_res) == "5"

    def test_exclude_end(self, space):
        w_res = space.execute("return (1..5).exclude_end?")
        assert self.unwrap(space, w_res) is False

        w_res = space.execute("return (1...5).exclude_end?")
        assert self.unwrap(space, w_res) is True

    def test_eql(self, space):
        w_res = space.execute("return (1..2) == (1..2)")
        assert self.unwrap(space, w_res) is True

        w_res = space.execute("return (1...2) == (1...2)")
        assert self.unwrap(space, w_res) is True

        w_res = space.execute("return (1..2) == 4")
        assert self.unwrap(space, w_res) is False

        w_res = space.execute("return (1..2) == Range.new(1, 2)")
        assert self.unwrap(space, w_res) is True

        w_res = space.execute("return (1..2) == Range.new(1, 2, false)")
        assert self.unwrap(space, w_res) is True

        w_res = space.execute("return (1...2) == Range.new(1, 2, true)")
        assert self.unwrap(space, w_res) is True

        w_res = space.execute("return (1..2) == (1...2)")
        assert self.unwrap(space, w_res) is False

    def test_eql_eql(self, space):
        w_res = space.execute("return (1..2) === 1")
        assert self.unwrap(space, w_res) is True

        w_res = space.execute("return (1..2) === 3")
        assert self.unwrap(space, w_res) is False

    def test_include(self, space):
        w_res = space.execute("return (1..5).member?(4)")
        assert self.unwrap(space, w_res) is True

        w_res = space.execute("return (1..5).member?(6)")
        assert self.unwrap(space, w_res) is False

        w_res = space.execute("return ('1'..'5').member?('2')")
        assert self.unwrap(space, w_res) is True

        w_res = space.execute("return ('1'..'5').member?('6')")
        assert self.unwrap(space, w_res) is False

        w_res = space.execute("return ('a'..'f').member?('c')")
        assert self.unwrap(space, w_res) is True

    def test_cover(self, space):
        w_res = space.execute("return (1..2).cover?(0)")
        assert self.unwrap(space, w_res) is False
        w_res = space.execute("return (1..2).cover?(1)")
        assert self.unwrap(space, w_res) is True
        w_res = space.execute("return (1..2).cover?(2)")
        assert self.unwrap(space, w_res) is True
        w_res = space.execute("return (1..2).cover?(3)")
        assert self.unwrap(space, w_res) is False

        w_res = space.execute("return (1...2).cover?(0)")
        assert self.unwrap(space, w_res) is False
        w_res = space.execute("return (1...2).cover?(1)")
        assert self.unwrap(space, w_res) is True
        w_res = space.execute("return (1...2).cover?(2)")
        assert self.unwrap(space, w_res) is False

    def test_allocate(self, space):
        w_res = space.execute("return Range.allocate.begin")
        assert self.unwrap(space, w_res) is None

        w_res = space.execute("return Range.allocate.end")
        assert self.unwrap(space, w_res) is None

        w_res = space.execute("return Range.allocate.exclude_end?")
        assert self.unwrap(space, w_res) is False

    def test_new(self, space):
        w_res = space.execute("return Range.new(1, 2).begin")
        assert self.unwrap(space, w_res) == 1
        w_res = space.execute("return Range.new(1, 2).end")
        assert self.unwrap(space, w_res) == 2
        w_res = space.execute("return Range.new(1, 2).exclude_end?")
        assert self.unwrap(space, w_res) is False

        w_res = space.execute("return Range.new(1, 2, true).begin")
        assert self.unwrap(space, w_res) == 1
        w_res = space.execute("return Range.new(1, 2, true).end")
        assert self.unwrap(space, w_res) == 2
        w_res = space.execute("return Range.new(1, 2, true).exclude_end?")
        assert self.unwrap(space, w_res) is True

import unittest


def join_left(left_set, right_set):
    return _nested_join(left_set, right_set, _left_compose)


def _left_compose(key, primary, secondary):
    return key, primary, secondary


def join_right(left_set, right_set):
    return _nested_join(right_set, left_set, _right_compose)


def _right_compose(key, primary, secondary):
    return key, secondary, primary


def _nested_join(primary, secondary, compose):
    return {compose(key, val, _retrieve_value_from_set(key, secondary)) for (key, val) in primary}


def _retrieve_value_from_set(key, secondary):
    return next(_extract_value(key, secondary), None)


def _extract_value(key, secondary):
    return map(lambda pair: pair[1], _find_pair_by_key(secondary, key))


def _find_pair_by_key(secondary, key):
    return filter(lambda pair: pair[0] == key, secondary)


class NestedJoinsTest(unittest.TestCase):
    def testResultSetIsEmpty_whenJoinLeftTwoEmptyLists(self):
        self.assertEqual(set(), join_left(set(), set()))

    def testResultSetHasNonesOnRight_whenJoinLeftNonemptyAndEmptySets(self):
        self.assertEqual(
            {(1, 'l1', None), (2, 'l2', None), (3, 'l3', None)},
            join_left(
                {(1, 'l1'), (2, 'l2'), (3, 'l3')},
                set()
            )
        )

    def testResultSetHasValuesOnRight_forCorrespondingKeys_whenJoinLeftTwoNonemptySets(self):
        self.assertEqual(
            {(1, 'l1', 'r1'), (2, 'l2', None), (3, 'l3', 'r3')},
            join_left(
                {(1, 'l1'), (2, 'l2'), (3, 'l3')},
                {(1, 'r1'), (3, 'r3')}
            )
        )

    def testResultSetIsEmpty_whenJoinRightTwoEmptySets(self):
        self.assertEqual(set(), join_right(set(), set()))

    def testResultSetHasNonesOnLeft_whenJoinRightEmptyAndNonemptySets(self):
        self.assertEqual(
            {(1, None, 'r1'), (2, None, 'r2'), (3, None, 'r3')},
            join_right(
                set(),
                {(1, 'r1'), (2, 'r2'), (3, 'r3')}
            )
        )

    def testResultSetHasValues_forCorrespondingKeys_whenJoinRightTwoNonemptySets(self):
        self.assertEqual(
            {(1, 'l1', 'r1'), (2, None, 'r2'), (3, 'l3', 'r3')},
            join_right(
                {(1, 'l1'), (3, 'l3')},
                {(1, 'r1'), (2, 'r2'), (3, 'r3')}
            )
        )

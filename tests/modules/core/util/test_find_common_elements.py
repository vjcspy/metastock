from metastock.modules.core.util.find_common_elements import find_common_elements


def test_empty_lists():
    assert find_common_elements() == []
    assert find_common_elements([]) == []
    assert find_common_elements([], []) == []


def test_single_list():
    assert find_common_elements([1, 2, 3]) == [1, 2, 3]


def test_no_common_elements():
    assert find_common_elements([1, 2], [3, 4], [5, 6]) == []


def test_some_common_elements():
    assert set(find_common_elements([1, 2, 3], [3, 4, 5], [5, 6, 3])) == {3}


def test_all_common_elements():
    assert set(find_common_elements([1, 2, 3], [1, 2, 3], [1, 2, 3])) == {1, 2, 3}


def test_mixed_types():
    assert find_common_elements([1, 'a'], ['a', 1]) == [1, 'a'] or ['a', 1]

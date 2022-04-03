import json

from speedscope_to_codeperf.schema.speedscope import get_cpu_by_function, get_flamegraph


def test_get_cpu_by_function():
    with open("./tests/two-sampled.speedscope.0.6.0.json", "r") as fd:
        json_data = json.load(fd)
        js = get_cpu_by_function(json_data)
        assert js == {
            "data": [
                {"symbol": "c", "flat%": "66.67", "cum%": "66.67"},
                {"symbol": "d", "flat%": "33.33", "cum%": "33.33"},
                {"symbol": "a", "flat%": "0.00", "cum%": "100.00"},
                {"symbol": "b", "flat%": "0.00", "cum%": "100.00"},
            ],
            "totalRows": 4,
            "totalPages": 1,
            "labels": [],
        }
    with open("./tests/sampled.speedscope.json", "r") as fd:
        json_data = json.load(fd)
        js = get_cpu_by_function(json_data, "lines")
        assert js == {
            "data": [
                {"symbol": "c:1", "flat%": "66.67", "cum%": "66.67"},
                {"symbol": "c:2", "flat%": "33.33", "cum%": "33.33"},
                {"symbol": "a:1", "flat%": "0.00", "cum%": "100.00"},
                {"symbol": "b:1", "flat%": "0.00", "cum%": "100.00"},
            ],
            "totalRows": 4,
            "totalPages": 1,
            "labels": [],
        }


def test_get_flamegraph():
    with open("./tests/sampled.speedscope.json", "r") as fd:
        json_data = json.load(fd)
        flame = get_flamegraph(json_data)
        assert flame == {
            "n": "root",
            "f": "root",
            "v": 0,
            "c": [
                {
                    "n": "a:1",
                    "f": "a:1",
                    "v": 0,
                    "c": [
                        {
                            "n": "b:1",
                            "f": "b:1",
                            "v": 0,
                            "c": [
                                {"n": "c:1", "f": "c:1", "v": 2, "c": []},
                                {"n": "c:2", "f": "c:2", "v": 1, "c": []},
                            ],
                        }
                    ],
                }
            ],
        }

# Benchmarks

This directory contains performance benchmarks for the `mdit-py-figure` markdown extension.

## Running Benchmarks

First, install the development dependencies including `pytest-benchmark`:

```bash
uv sync --group dev
```

Then run all benchmarks:

```bash
pytest benchmarks/ --benchmark-only
```

### Running Specific Benchmark Classes

Run only basic benchmarks:
```bash
pytest benchmarks/test_figure_benchmarks.py::TestBasicFigureBenchmarks --benchmark-only
```

Run scalability benchmarks:
```bash
pytest benchmarks/test_figure_benchmarks.py::TestScalabilityBenchmarks --benchmark-only
```

### Comparing Results

To save benchmark results for comparison:
```bash
pytest benchmarks/ --benchmark-save=baseline
```

Then make changes and compare:
```bash
pytest benchmarks/ --benchmark-compare=baseline
```

## Benchmark Categories

### TestBasicFigureBenchmarks
Tests basic figure parsing scenarios:
- Single image with caption
- Multiple images with caption
- Image without caption
- Complex caption formatting

### TestLargeDocumentBenchmarks
Tests performance on larger documents:
- Large document with many figures (~80 figures)
- Baseline comparison without plugin

### TestPluginOptionsBenchmarks
Tests different plugin configurations:
- `image_link` option enabled
- `skip_no_caption` option enabled
- Both options enabled

### TestComparisonBenchmarks
Direct comparison with and without the plugin to measure overhead.

### TestScalabilityBenchmarks
Tests how performance scales with input size:
- Multiple images in a single figure (1, 5, 10, 20, 50 images)
- Multiple separate figures (1, 10, 50, 100 figures)

### TestMixedContentBenchmarks
Tests realistic documents with mixed content types (headings, lists, blockquotes, code blocks, and figures).

## Benchmark Options

### Useful pytest-benchmark options:

- `--benchmark-only`: Skip test assertions, only run benchmarks
- `--benchmark-min-rounds=N`: Set minimum number of rounds (default: 5)
- `--benchmark-min-time=T`: Set minimum time per benchmark (default: 0.000005)
- `--benchmark-compare=NAME`: Compare against saved results
- `--benchmark-autosave`: Automatically save results
- `--benchmark-histogram=FILENAME`: Generate histogram

Example with custom settings:
```bash
pytest benchmarks/ --benchmark-only --benchmark-min-rounds=10 --benchmark-histogram=hist
```

## Understanding Results

Benchmark results include:
- **Min**: Minimum execution time
- **Max**: Maximum execution time
- **Mean**: Average execution time
- **StdDev**: Standard deviation
- **Median**: Median execution time
- **IQR**: Interquartile range
- **Outliers**: Number of outlier measurements
- **Rounds**: Number of benchmark rounds
- **Iterations**: Iterations per round

## Performance Goals

The figure plugin should have minimal overhead:
- Basic single-figure parsing: < 1ms
- Large documents (80 figures): < 50ms
- Plugin overhead vs baseline: < 10%

These are rough guidelines and actual performance will vary by system.

"""Benchmarks for the figure plugin."""

import pytest
from markdown_it import MarkdownIt
from mdit_py_figure import figure_plugin


# Sample markdown texts of varying complexity
SINGLE_IMAGE_CAPTION = """![Picture of Oscar.](/path/to/cat.jpg)
Awesome caption about **Oscar** the kitty."""

MULTIPLE_IMAGES_CAPTION = """![Picture of Oscar.](/path/to/cat1.jpg)
![Picture of Luna.](/path/to/cat2.jpg)
![Picture of Oreo.](/path/to/cat3.jpg)
Awesome captions about the **kitties**."""

COMPLEX_CAPTION = """![Image](image.png)
This is a **complex** caption with *italic*, [links](https://example.com), and `code` formatting."""

NO_CAPTION = "![Alt text](https://example.com/image.jpg)"

# Large document with multiple figures
LARGE_DOCUMENT = """
# Introduction

Some introductory text here.

![First image](/img1.png)
Caption for the first image.

## Section 1

More content and discussion.

![Second image](/img2.png)
![Third image](/img3.png)
Multiple images with a shared caption.

### Subsection

Additional content here with **bold** and *italic* text.

![Fourth image](/img4.png)
Another figure with caption.

![Fifth image](/img5.png)
Yet another figure.

## Section 2

![Sixth image](/img6.png)
![Seventh image](/img7.png)
![Eighth image](/img8.png)
Three images sharing one caption.

Final paragraph of text.
""" * 10  # Repeat 10 times for a larger document


class TestBasicFigureBenchmarks:
    """Benchmark basic figure parsing scenarios."""

    def test_single_image_with_caption(self, benchmark):
        """Benchmark parsing single image with caption."""
        md = MarkdownIt().use(figure_plugin)
        result = benchmark(md.render, SINGLE_IMAGE_CAPTION)
        assert "<figure>" in result
        assert "<figcaption>" in result

    def test_multiple_images_with_caption(self, benchmark):
        """Benchmark parsing multiple images with caption."""
        md = MarkdownIt().use(figure_plugin)
        result = benchmark(md.render, MULTIPLE_IMAGES_CAPTION)
        assert result.count("<img") == 3
        assert "<figcaption>" in result

    def test_image_no_caption(self, benchmark):
        """Benchmark parsing image without caption."""
        md = MarkdownIt().use(figure_plugin)
        result = benchmark(md.render, NO_CAPTION)
        assert "<figure>" in result

    def test_complex_caption_formatting(self, benchmark):
        """Benchmark parsing caption with complex markdown formatting."""
        md = MarkdownIt().use(figure_plugin)
        result = benchmark(md.render, COMPLEX_CAPTION)
        assert "<strong>" in result
        assert "<em>" in result
        assert "<a href=" in result


class TestLargeDocumentBenchmarks:
    """Benchmark performance on larger documents."""

    def test_large_document_with_many_figures(self, benchmark):
        """Benchmark parsing large document with multiple figures."""
        md = MarkdownIt().use(figure_plugin)
        result = benchmark(md.render, LARGE_DOCUMENT)
        # Should have many figures (50 in total: 5 figures per iteration × 10 repetitions)
        assert result.count("<figure>") == 50

    def test_large_document_baseline(self, benchmark):
        """Benchmark parsing large document without figure plugin (baseline)."""
        md = MarkdownIt()
        result = benchmark(md.render, LARGE_DOCUMENT)
        # Without plugin, images should be in <p> tags
        assert "<figure>" not in result


class TestPluginOptionsBenchmarks:
    """Benchmark different plugin configurations."""

    def test_image_link_option(self, benchmark):
        """Benchmark with image_link option enabled."""
        md = MarkdownIt().use(figure_plugin, image_link=True)
        result = benchmark(md.render, SINGLE_IMAGE_CAPTION)
        assert '<a href="/path/to/cat.jpg">' in result

    def test_skip_no_caption_option(self, benchmark):
        """Benchmark with skip_no_caption option enabled."""
        md = MarkdownIt().use(figure_plugin, skip_no_caption=True)
        result = benchmark(md.render, NO_CAPTION)
        # Should NOT transform to figure
        assert "<figure>" not in result

    def test_both_options_enabled(self, benchmark):
        """Benchmark with both image_link and skip_no_caption enabled."""
        md = MarkdownIt().use(figure_plugin, image_link=True, skip_no_caption=True)
        result = benchmark(md.render, SINGLE_IMAGE_CAPTION)
        assert "<figure>" in result
        assert '<a href="/path/to/cat.jpg">' in result


class TestComparisonBenchmarks:
    """Benchmark comparison with and without plugin."""

    def test_with_plugin(self, benchmark):
        """Benchmark markdown rendering WITH figure plugin."""
        md = MarkdownIt().use(figure_plugin)
        benchmark(md.render, SINGLE_IMAGE_CAPTION)

    def test_without_plugin(self, benchmark):
        """Benchmark markdown rendering WITHOUT figure plugin (baseline)."""
        md = MarkdownIt()
        benchmark(md.render, SINGLE_IMAGE_CAPTION)


class TestScalabilityBenchmarks:
    """Benchmark scalability with different input sizes."""

    @pytest.mark.parametrize("num_images", [1, 5, 10, 20, 50])
    def test_multiple_images_scaling(self, benchmark, num_images):
        """Benchmark how performance scales with number of images."""
        # Generate markdown with N images
        images = "\n".join([f"![Image {i}](/img{i}.png)" for i in range(num_images)])
        markdown = f"{images}\nShared caption for all images."

        md = MarkdownIt().use(figure_plugin)
        result = benchmark(md.render, markdown)
        assert result.count("<img") == num_images

    @pytest.mark.parametrize("num_figures", [1, 10, 50, 100])
    def test_multiple_figures_scaling(self, benchmark, num_figures):
        """Benchmark how performance scales with number of separate figures."""
        # Generate markdown with N separate figures
        figures = []
        for i in range(num_figures):
            figures.append(f"![Image {i}](/img{i}.png)")
            figures.append(f"Caption for image {i}.")
            figures.append("")  # Empty line to separate figures

        markdown = "\n".join(figures)

        md = MarkdownIt().use(figure_plugin)
        result = benchmark(md.render, markdown)
        assert result.count("<figure>") == num_figures


class TestMixedContentBenchmarks:
    """Benchmark documents with mixed content types."""

    def test_mixed_content_document(self, benchmark):
        """Benchmark document with figures mixed with other content."""
        markdown = """
# Title

Regular paragraph with some text.

- List item 1
- List item 2
- List item 3

![Image 1](img1.png)
Caption for image 1.

> This is a blockquote
> with multiple lines.

![Image 2](img2.png)
![Image 3](img3.png)
Shared caption.

```python
def hello():
    print("code block")
```

Regular paragraph.

![Image 4](img4.png)
Final caption.
"""
        md = MarkdownIt().use(figure_plugin)
        result = benchmark(md.render, markdown)
        assert result.count("<figure>") == 3

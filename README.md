<div align="center">
  <img src="/.github/images/github-header-image.webp#gh-dark-mode-only" alt="GitHub Header Image" width="auto" />
  <img src="/.github/images/github-header-image-light.webp#gh-light-mode-only" alt="GitHub Header Image" width="auto" />
  
  <!-- Badges -->
  <p></p> 
  <a href="https://ull.es">
    <img
      alt="License"
      src="https://img.shields.io/badge/ULL-5C068C?style=for-the-badge&logo=gitbook&labelColor=302D41"
    />
  </a>
  <a href="https://github.com/hadronomy/PR1-IA-2425/blob/main/LICENSE">
    <img
      alt="License"
      src="https://img.shields.io/badge/MIT-EE999F?style=for-the-badge&logo=starship&label=LICENSE&labelColor=302D41"
    />
  </a>
  <p></p>
  <!-- TOC -->
  <a href="#docs">Docs</a> •
  <a href="#build">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#license">License</a>
  <hr />
</div>

## Docs

See the [docs](/docs/README.md) for more information.

## Installation

Download the latest release from the [releases](https://github.com/hadronomy/PR1-IA-2425/releases/latest) page.
Or proceed if you have the wheel file.

```bash
pip install ia-0.1.0-py3-none-any.whl
```

or

```bash
pipx install ia-0.1.0-py3-none-any.whl
```

## Usage

<details>
<summary>

### Without installation

</summary>


To ensure the appropriate environment is set up, we use [Poetry](https://python-poetry.org/).

#### 1. Install Poetry

```bash
pipx install poetry
```

#### 2. Clone the repository and navigate to the project directory

```bash
git clone git@github.com:hadronomy/PR1-IA-2425.git
cd PR1-IA-2425
```

#### 3. Install the dependencies and create a virtual environment

```bash
poetry install
```

#### 4. Activate the virtual environment

```bash
poetry shell
```

#### 5. Run the application

```bash
ia --help
```

or

```bash
python -m ia --help
```
</details>

<details>
<summary>

### With installation

</summary>

#### Run the application

```bash
ia --help
```

or

```bash
python -m ia --help
```

</details>

## License

This project is licensed under the MIT License -
see the [LICENSE](/LICENSE) file for details.

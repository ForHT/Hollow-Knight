This is a game project based on python, borrowed from a C++ project - Hollow Knight.

Original project address: https://www.bilibili.com/video/BV1kz421m7RQ/?spm_id_from=333.337.search-card.all.click&vd_source=b49a3a4dd8cdbbf40d25251

## Requirements

Before running the project, you need to install the necessary dependencies and set up the environment.

### Setting Up

1. **Create a Conda Environment**:
   First, create a new Conda environment with Python 3.9:

   ```bash
   conda create -n hollow_knight python=3.9
   ```

2. **Activate the Conda Environment**:
   Once the environment is created, activate it:

   ```bash
   conda activate hollow_knight
   ```

3. **Install Dependencies**:
   After activating the environment, install all the required dependencies listed in `requirements.txt` using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Game**:
   Finally, you can start the game by running the `main.py` script:

   ```bash
   python main.py
   ```

## Controls

* **Movement**:

  * `W` – Move Up
  * `A` – Move Left
  * `S` – Move Down
  * `D` – Move Right
* **Actions**:

  * `J` – Attack
  * `K` – Jump
  * `L` – Dodge

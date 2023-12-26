Contributing Guide for Developers

Setting Up the Development Environment
--------------------------------------
1. Clone the Repository:
	 ```bash
	 git clone https://github.com/your_username/your_project.git
	 cd your_project
	 ```
2. Set Up a Conda Environment:
	- Install Miniconda or Anaconda.
	- Create a new Conda environment:
        ```bash
        conda create -n your_env_name python=3.11
	    conda activate your_env_name
        ```

3. Install Dependencies:
    ```bash
	pip install -r requirements.txt
    ```

Setting Up Pre-commit
---------------------
1. Install Pre-commit:
	```bash
    pip install pre-commit
    ```

2. Install Git Hooks:
	```bash
    pre-commit install
    ```

3. Run Pre-commit Manually (Optional):
	```bash
    pre-commit run --all-files
    ```

Making Changes and Opening a Pull Request
-----------------------------------------
1. Create a New Branch:
	```bash
    git checkout -b your_feature_branch
    ```

2. Make Your Changes: Implement your feature or fix.

3. Test out the app:
	```bash
	# optionally
	export FLIP_FLIP_DEV_MODE=True
	export FLIP_FLOP_PORT=1234
	python -m src.app
	```

3. Run Tests:
	```bash
    pytest
    ```

4. Push Your Changes:
	```bash
    git push origin your_feature_branch
    ```

5. Open a Pull Request (PR):
	- Go to the repository on GitHub.
	- Open a PR against the stg branch for initial review.
	- Ensure CI checks pass and address any feedback from reviewers.

6. Merging to stg and Eventually to main:
	- Once approved, the changes will be merged into stg.
	- Periodically, stg will be merged into main after thorough testing.

Best Practices
--------------
- Ensure your code is well-commented and follows the project's coding standards.
- Include unit tests for new features or bug fixes.
- Keep PRs small and focused for easier review.
- Update or add to the documentation as needed.

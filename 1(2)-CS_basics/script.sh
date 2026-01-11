#!/bin/bash

# anaconda(또는 miniconda)가 존재하지 않을 경우 설치해주세요!
if ! command -v conda &> /dev/null; then
    echo "[INFO] conda가 설치되어 있지 않습니다. Miniconda 설치를 시작합니다..."
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
    bash miniconda.sh -b -p $HOME/miniconda3
    source "$HOME/miniconda3/etc/profile.d/conda.sh"
    rm miniconda.sh
    echo "[INFO] Miniconda 설치 완료."
else
    CONDA_BASE=$(conda info --base 2>/dev/null)
    if [ -n "$CONDA_BASE" ] && [ -f "$CONDA_BASE/etc/profile.d/conda.sh" ]; then
        source "$CONDA_BASE/etc/profile.d/conda.sh"
    elif [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
        source "$HOME/miniconda3/etc/profile.d/conda.sh"
    else
        eval "$(conda shell.bash hook)"
    fi
    echo "[INFO] conda가 이미 설치되어 있습니다."
fi

# Conda 환셩 생성 및 활성화
conda create -n myenv python=3.10 -y ||true
conda activate myenv
export PATH="$HOME/miniconda3/envs/myenv/bin:$PATH"

## 건드리지 마세요! ##
python_env=$(python -c "import sys; print(sys.prefix)")
if [[ "$python_env" == *"/envs/myenv"* ]]; then
    echo "[INFO] 가상환경 활성화: 성공"
else
    echo "[INFO] 가상환경 활성화: 실패"
    exit 1 
fi

# 필요한 패키지 설치
pip install mypy

# Submission 폴더 파일 실행
cd submission || { echo "[INFO] submission 디렉토리로 이동 실패"; exit 1; }

for file in *.py; do
    filename=$(basename "$file" .py)
    
    input_file="../input/${filename}_input"
    output_file="../output/${filename}_output"
    
    if [ -f "$input_file" ]; then
        echo "[RUN] Running $file with input $input_file..."
        python "$file" < "$input_file" > "$output_file"
    else
        echo "[WARN] Input file not found for $file"
    fi
done

# mypy 테스트 실행 및 mypy_log.txt 저장
mypy *.py > ../mypy_log.txt

# conda.yml 파일 생성
conda env export --name myenv --file ../conda.yml

# 가상환경 비활성화
conda deactivate 
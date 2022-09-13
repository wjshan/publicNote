# Git

## 提交前进行单元测试和格式检查

```bash
ENV_PREFIX="$(pwd)/venv/bin/python"
if [ ! -f "$ENV_PREFIX" ]; then
    ENV_PREFIX="python3"
fi

$ENV_PREFIX -V

$ENV_PREFIX manage.py test > /dev/null # 执行单元测试
test_result=$? # 获取单元测试的返回结果 0-成功,1-失败
echo "****************************************"
if [  $test_result -ne 0 ]; then # 当单元测试失败,则终止此次提交
  echo "单元测试失败"
  exit 1
fi
change_files=$(git diff --name-only --cached --diff-filter=ACM -- '*.py') # 获取本次提交修改的文件
if [ "$change_files" != "" ] # 存在文件修改
then
    echo "$change_files"
    $ENV_PREFIX -m autoflake -i --remove-all-unused-imports --ignore-init-module-imports $change_files # 格式化导入,移除未使用的导入
    $ENV_PREFIX -m black $change_files # 格式化代码
    flake_errors=$($ENV_PREFIX -m flake8 $change_files) # 检测代码格式问题

    if [ 0 == "$flake_errors" ]
    then
      echo "flake8 no problem"
    else
      echo "$flake_errors" # 代码格式存在问题,终止此次提交
      exit 1
    fi
    git add $change_files # 格式化修改后的文件再次加入到暂存区中
fi
exit 0

```
/*
 * @Author: Luxiu123 klt5466@163.com
 * @Date: 2022-06-29 20:09:49
 * @Description: git 尝试 Push，失败自动重试
 * 命令行参数：
 *     [1]: git 仓库根目录
 *     [2]: git 命令
 */

const process = require("process");
const childProcess = require("child_process");
const log = require("loglevel");
log.setLevel("debug");
// 命令行参数
const cwd = process.argv[2];
const cmd = process.argv[3];
let failedTimes = 1;
// 执行函数
const pushFunc = () => {
  try {
    let output = childProcess
      .execSync(cmd, {
        shell: "powershell",
        cwd: cwd,
      })
      .toString();
    log.debug(output);
    return output;
  } catch (error) {
    // 带红色输出
    log.debug("\x1B[31m" + `>>> error ${failedTimes++} times` + "\x1B[37m");
    return error.toString();
  }
};
// 当有错误发生时，重复调用
while (pushFunc().toString().includes("fatal:"));
log.info("over");

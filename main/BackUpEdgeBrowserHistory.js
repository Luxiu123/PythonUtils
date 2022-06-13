/*
 * @Author: Luxiu123 klt5466@163.com
 * @Date: 2022-06-06 17:29:31
 * @Description: Edge浏览器历史记录备份
 */
const config = require("./config/Config");
const fs = require("fs");
const path = require("path");
const moment = require("moment");
const log = require("loglevel");
const archiver = require("archiver");
const { exit } = require("process");

log.setLevel("debug");
// 当日日期
const CurrentDate = moment(new Date().getTime(), "x").format("YYYY-MM-DD");
// 目的目录
const DestDir = "E:/document/DataBase/edge/" + CurrentDate;
// 创建目的文件夹
if (!fs.existsSync(DestDir)) {
  fs.mkdirSync(DestDir);
}
log.debug(`创建目的文件夹${DestDir}成功`);
// Edge 目录
const EdgeDefaultDirectory = `C:/Users/${config.currentHostName}/AppData/Local/Microsoft/Edge/User Data/Default`;
// 源文件名
const SourceFiles = fs.readdirSync(EdgeDefaultDirectory).filter((v) => {
  return fs.statSync(path.join(EdgeDefaultDirectory, v)).isFile();
});
// 复制到目的目录
log.trace(`复制文件到 ${DestDir} ...`);
SourceFiles.map((v) => {
  fs.copyFileSync(path.join(EdgeDefaultDirectory, v), path.join(DestDir, v));
  log.trace(`复制文件 ${v} 成功`);
});
log.debug(`复制文件到 ${DestDir} 成功`);

// 压缩文件
const DestZipFile = path.join(path.dirname(DestDir), `${CurrentDate}.zip`);
const output = fs.createWriteStream(DestZipFile);
const archive = archiver("zip", {
  zlib: { level: 9 }, // Sets the compression level.
});
// 监听结束事件
let finished = false;
output.on("close", function () {
  console.log("finished");
  // 删除目的目录
  fs.rmSync(DestDir, { recursive: true });
  finished = true;
});
archive.pipe(output);
// 添加文件到压缩包
fs.readdirSync(DestDir).map((v) => {
  archive.append(fs.createReadStream(path.join(DestDir, v)), { name: v });
});
archive.finalize();
// 等待执行结束
setInterval(() => {
  if (finished) {
    exit(0);
  }
}, 250);

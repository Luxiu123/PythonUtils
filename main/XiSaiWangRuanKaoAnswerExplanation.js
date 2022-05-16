/*希赛网软考，题目+答案解析，用于笔记*/

let space = String.fromCharCode(0xa0);
let source =
  document.querySelector("#paperWrap").innerText +
  "\n" +
  document.querySelector("#jiexispan").innerText;
source = source
  .replaceAll(space, " ")
  .replace("问题1", "")
  .replace(/问题\d+/g, " ")
  .replace(/第\d+题（单选题）：/g, "")
  .replace("收藏 \n纠错", " ")
  .replace(/\n\n+/g, "\n");
let answers = [];
for (const elem of document.querySelectorAll(
  "#paperWrap2 div.answerEnd>div.daan_sty"
)) {
  answers.push(
    elem.querySelector("div.div2>p:first-child>span:last-child").innerText
  );
}
let count = 0;
// 填充答案
source = source.replace(/（\s+）/g, (match) => {
  return `（ ${answers[count++]} ）`;
});
// 去除选项字母序号
source = source.replace(/ \w\.(?<content>.*\n)/g, "$<content>");
console.log(source + "\n");

const simpleGit = require('simple-git/promise');


// 克隆仓库
async function cloneRepository(repoUrl, localPath) {
  try {
    await simpleGit().clone(repoUrl, localPath);
    console.log('Repository cloned successfully.');
  } catch (error) {
    console.error('Error:', error);
  }
}

// 提交更改
async function commitChanges(localPath, message) {
  const git = simpleGit(localPath);
  try {
    await git.add(['.']);
    await git.commit(message);
    console.log('Changes committed successfully.');
  } catch (error) {
    console.error('Error:', error);
  }
}

// 推送代码
async function pushChanges(localPath) {
  const git = simpleGit(localPath);
  try {
    await git.push('origin', 'main');
    console.log('Changes pushed successfully.');
  } catch (error) {
    console.error('Error:', error);
  }
}


export function commitAndPush() {
  // 示例用法
  const repoUrl = 'https://r.danim.space/d/snote-1.git';
  const localPath = '/meds/meds-2024c.txt';

  // 克隆仓库
  cloneRepository(repoUrl, localPath);

  // 进入本地仓库目录
  process.chdir(localPath);

  // 修改文件后提交
  commitChanges(localPath, 'Commit and push from temp web committer');

  // 推送更改
  pushChanges(localPath);
}

export default commitAndPush;
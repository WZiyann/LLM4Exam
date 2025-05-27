// App.jsx
import { useState } from 'react'
import axios from 'axios'

export default function App() {
  const [subject, setSubject] = useState("数学")
  const [grade, setGrade] = useState("初中")
  const [questionType, setType] = useState("选择题")
  const [prompt, setPrompt] = useState("生成5道概率相关题目")
  const [file, setFile] = useState("")

  const generate = async () => {
    const res = await axios.post("/generate", {
      subject, grade, question_type: questionType, prompt, count: 5
    })
    setFile(res.data.file)
  }

  return (
    <div>
      <h1>试题生成系统</h1>
      <input placeholder="学科" value={subject} onChange={e => setSubject(e.target.value)} />
      <input placeholder="年级" value={grade} onChange={e => setGrade(e.target.value)} />
      <input placeholder="类型" value={questionType} onChange={e => setType(e.target.value)} />
      <textarea value={prompt} onChange={e => setPrompt(e.target.value)} />
      <button onClick={generate}>生成试卷</button>
      {file && <a href={`/download?path=${file}`}>下载试卷</a>}
    </div>
  )
}

import React, { useState } from 'react';
import axios from 'axios';

const apiUrl = "http://backend:8000";

function App() {
  const [count, setCount] = useState(0);

  // 숫자 표시 업데이트
  const updateDisplay = (newCount) => {
    setCount(newCount);
  };

  // MongoDB에 count 값 저장하는 함수
  async function saveCount(newCount) {
    try {
      const response = await fetch(`${apiUrl}/count`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ count: newCount }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      console.log(data.message);
    } catch (error) {
      console.error("Error:", error);
    }
  }

  // 카운트를 증가시키는 함수
  const increase = async () => {
    const newCount = count + 1;
    updateDisplay(newCount);
    await saveCount(newCount);
  };

  // 카운트를 감소시키는 함수
  const decrease = async () => {
    const newCount = count - 1;
    updateDisplay(newCount);
    await saveCount(newCount);
  };

  return (
    <div>
      <h1>결과: <span id="numberDisplay">{count}</span></h1>
      <button onClick={increase}>+</button>
      <button onClick={decrease}>-</button>
    </div>
  );
}

export default App;

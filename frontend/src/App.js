import React, { useState, useEffect } from 'react';
import axios from 'axios';

const apiUrl = "http://backend:8000";

function App() {
  const [count, setCount] = useState(0);

  // 초기 count 값 가져오기
  useEffect(() => {
    axios.get(`${apiUrl}/count`)
      .then((response) => {
        setCount(response.data.count);
      })
      .catch((error) => {
        console.error("Error fetching count:", error);
      });
  }, []);

  // 카운트를 증가시키는 함수
  const increaseCount = () => {
    axios.post(`${apiUrl}/increase`)
      .then((response) => {
        setCount(response.data.count);
      })
      .catch((error) => {
        console.error("Error increasing count:", error);
      });
  };

  // 카운트를 감소시키는 함수
  const decreaseCount = () => {
    axios.post(`${apiUrl}/decrease`)
      .then((response) => {
        setCount(response.data.count);
      })
      .catch((error) => {
        console.error("Error decreasing count:", error);
      });
  };

  return (
    <div>
      <h1>결과: {count}</h1>
      <button onClick={increaseCount}>+</button>
      <button onClick={decreaseCount}>-</button>
    </div>
  );
}

export default App;

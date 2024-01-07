import { useEffect, useState } from "react";
import "./App.css";

const eventSource = new EventSource("/stream/");

function App() {
  const [messages, setMessages] = useState<readonly string[]>([]);

  function eventHandler(event: MessageEvent<any>) {
    const data = event.data;

    // CLOSE event is not in SSE specification
    // this is just a convention that can be used to terminate a SSE stream
    if (data === "CLOSE") {
      eventSource.close();
      return;
    }

    setMessages((previous) => [...previous, data]);
  }

  useEffect(() => {
    eventSource.addEventListener("message", eventHandler);

    return () => {
      eventSource.removeEventListener("message", eventHandler);
    };
  }, []);

  return (
    <>
      {messages.map((message, i) => {
        return <p key={i}>{`${i}. ${message}`}</p>;
      })}
    </>
  );
}

export default App;

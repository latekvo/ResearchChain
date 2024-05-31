"use client";
import React from "react";
import Header from "../components/Header";
import { useQuery } from "react-query";
import { Card, CardBody, CardFooter, CardHeader, Divider } from "@nextui-org/react";
import { PiQueueDuotone } from "react-icons/pi";

interface CrawlHistoryItem {
  task: {
    uuid: string;
    prompt: string;
    mode: string;
    completed: boolean;
    completion_result: string | null;
    executing: boolean;
    required_crawl_tasks: string[];
    completion_date: number;
    execution_date: number;
    timestamp: number;
  }[];
}

const CrawlHistory = () => {
  // const { data, isLoading, isError } = useQuery<CrawlHistoryItem[], Error>(
  //   "crawlHistory",
  //   async () => {
  //     const response = await fetch("http://127.0.0.1:8000/crawl");
  //     if (!response.ok) {
  //       throw new Error("Failed to fetch crawl history");
  //     }
  //     return response.json();
  //   }
  // );

  const isLoading = false;
  const isError = false;
  const data: CrawlHistoryItem = {
    task: [
      {
        uuid: "test",
        prompt: "Huge prompt huge prompt huge prompt huge prompt huge prompt",
        mode: "Docs",
        completed: false,
        completion_result: null,
        executing: false,
        required_crawl_tasks: [],
        completion_date: 0,
        execution_date: 0,
        timestamp: 1717181223.387721,
      },
      {
        uuid: "test",
        prompt: "Huge prompt huge prompt huge prompt",
        mode: "Wiki",
        completed: true,
        completion_result: null,
        executing: false,
        required_crawl_tasks: [],
        completion_date: 0,
        execution_date: 0,
        timestamp: 1717184223.387721,
      },
    ],
  };

  if (isLoading) {
    return (
      <div className="h-screen w-screen">
        <Header></Header>
        <div className="text-center">Loading...</div>
      </div>
    );
  }

  if (isError) {
    return (
      <div className="h-screen w-screen">
        <Header></Header>
        <div className="text-center">Fetching data</div>
      </div>
    );
  }

  if (!data || data.task.length === 0) {
    return (
      <div className="h-screen w-screen">
        <Header></Header>
        <div className="text-center">There is no crawler history</div>
      </div>
    );
  }

  const calculateElapsedTime = (timestamp: number):string => {
    const now = new Date();
    const diffInMinutes = Math.floor((now.getTime() - timestamp) / (1000 * 60));
    if (diffInMinutes >= 60) {
      const diffInHours = parseInt((diffInMinutes / 60).toString(), 10);
      return `${diffInHours}\n Hour ago`;
    }
    return `${diffInMinutes}\n Minutes ago`;
  };

  return (
    <div className="h-screen w-screen flex-col">
      <Header></Header>
      <div className="h-4/5 w-full flex-col items-center justify-center">
        <div className="flex-col justify-center">
          {data.task.map((item) => (
            <Card key={item.uuid} className="p-2 m-2 w-1/3 mx-auto">
              <CardHeader>
                <div className="flex justify-between w-full">
                  <PiQueueDuotone color="yellow" className="text-3xl my-auto mr-6 rounded-full"></PiQueueDuotone>
                  <div className="flex flex-col">
                    <p className="text-md text-center">{item.mode}</p>
                    <p className="text-small text-default-500">Queued</p>
                  </div>
                  <div>
                    <p className="text-sm whitespace-pre-line text-center">{calculateElapsedTime(item.timestamp)}</p>
                  </div>
                </div>
              </CardHeader>
              <Divider/>
              <CardBody>
                <p>{item.prompt}</p>
              </CardBody>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};

export default CrawlHistory;

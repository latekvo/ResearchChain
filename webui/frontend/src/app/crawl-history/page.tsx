"use client";
import React from "react";
import Header from "../components/Header";
import { useQuery } from "react-query";
import { Card } from "@nextui-org/react";

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
        prompt: "test",
        mode: "test",
        completed: false,
        completion_result: null,
        executing: false,
        required_crawl_tasks: [],
        completion_date: 0,
        execution_date: 0,
        timestamp: 0,
      },
      {
        uuid: "test",
        prompt: "test",
        mode: "test",
        completed: false,
        completion_result: null,
        executing: false,
        required_crawl_tasks: [],
        completion_date: 0,
        execution_date: 0,
        timestamp: 0,
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

  return (
    <div className="h-screen w-screen flex-col">
      <Header></Header>
      <div className="h-4/5 w-full flex-col items-center justify-center">
        <h1>Crawl History</h1>
        <div className="flex-col justify-center">
          {data.task.map((item) => (
            <Card key={item.uuid} className="p-2 w-1/2 mx-auto">
              {item.prompt}
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};

export default CrawlHistory;

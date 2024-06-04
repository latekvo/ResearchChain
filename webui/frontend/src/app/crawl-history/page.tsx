"use client";
import React from "react";
import Header from "../components/Header";
import { useQuery } from "react-query";
import CrawlHistoryCard from "./CrawlHistoryCard";
import { data } from "./crawlHistoryMock";

export interface Task {
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
}

export interface CrawlHistoryItem {
  task: Task[];
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

  if (isLoading) {
    return (
      <div className="h-full w-full">
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
        <div className="grid grid-cols-4 gap-4 p-4">
          {data.task.map((item) => (
            <CrawlHistoryCard key={item.uuid} item={item}></CrawlHistoryCard>
          ))}
        </div>
      </div>
    </div>
  );
};

export default CrawlHistory;

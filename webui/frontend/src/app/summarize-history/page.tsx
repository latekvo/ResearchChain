"use client";
import React, { useState } from "react";
import Header from "../components/Header";
import { useQuery } from "react-query";
import HistoryCard from "../components/HistoryCard"
import { data } from "./SummarizeHistoryMock";
import SummarizeHistoryModal from "./SummarizeHistoryModal"
import { SummaryTask } from "../types/TaskType";


const SummarizeHistory = () => {

  const [selectedTaskIndex, setSelectedTaskIndex] = useState<number | null>(null);

  const handleCardClick = (index: number) => {
    setSelectedTaskIndex(index);
  };

  const closeModal = () => {
    setSelectedTaskIndex(null);
  };
  console.log(selectedTaskIndex);

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
      <Header />
      <div className="h-4/5 w-full flex-col items-center justify-center">
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 2xl:grid-cols-5 gap-4 p-4">
          {data.task.map((item, index) => (
            <div key={item.uuid}  onClick={() => handleCardClick(index)}>
              <HistoryCard item={item}></HistoryCard>
            </div>
          ))}
        </div>
      </div>

      {selectedTaskIndex && (
        <SummarizeHistoryModal
          isOpen={true}
          onClose={closeModal}
          summaryTask={data.task[selectedTaskIndex]}
        />
      )}
    </div>
  );
};

export default SummarizeHistory;

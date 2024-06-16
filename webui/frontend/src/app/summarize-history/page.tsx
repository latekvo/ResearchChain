"use client";
import React, { useState } from "react";
import Header from "../components/Header";
import { UseQueryResult, useQuery } from "react-query";
import HistoryCard from "../components/HistoryCard";
import SummarizeHistoryModal from "./SummarizeHistoryModal";
import { SummaryResult, SummaryTask } from "../types/TaskType";

const SummarizeHistory = () => {
  const [selectedTaskIndex, setSelectedTaskIndex] = useState<number | null>(
    null
  );

  const handleCardClick = (index: number) => {
    setSelectedTaskIndex(index);
  };

  const closeModal = () => {
    setSelectedTaskIndex(null);
  };

  const { data, isLoading, isError }: UseQueryResult<SummaryResult> = useQuery(
    "completionData",
    async (): Promise<SummaryResult> => {
      const response = await fetch("http://127.0.0.1:8000/completion");
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json() as Promise<SummaryResult>;
    }
  );

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

  if (!data || data.tasks.length === 0) {
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
          {data.tasks.map((item, index) => (
            <div
              key={item.uuid}
              className="cursor-pointer"
              onClick={() => handleCardClick(index)}
            >
              <HistoryCard item={item}></HistoryCard>
            </div>
          ))}
        </div>
      </div>

      {(selectedTaskIndex || selectedTaskIndex == 0) && (
        <SummarizeHistoryModal
          isOpen={true}
          onClose={closeModal}
          summaryTask={data.tasks[selectedTaskIndex]}
        />
      )}
    </div>
  );
};

export default SummarizeHistory;

"use client";
import React from "react";
import { Button, Tab, Tabs, Textarea } from "@nextui-org/react";

function PromptyInput() {
  return (
    <div className="w-1/2 p-5 shadow-xl rounded-xl border border-opacity-10 border-gray-400 bg-black bg-opacity-15 z-10 flex flex-col justify-between">
      <Textarea
        variant="underlined"
        placeholder="Ask a question :)"
        color="default"
        size="lg"
        minRows={1}
        className="text-gray-300 px-3 text-large whitespace-normal"
      />
      <div className="w-full mt-4 flex justify-between">
        <Tabs
          size="lg"
          aria-label="Options"
          variant="underlined"
          color="default"
        >
          <Tab key="news" title="News" />
          <Tab key="docs" title="Documentation" />
          <Tab key="wiki" title="Wikipedia" />
        </Tabs>
        <div className="w-2/3 mr-3 flex flex-row-reverse">
          <Button
            size="lg"
            type="submit"
            color="default"
            variant="bordered"
            className="w-2/3 mr-3 flex flex-row-reverse"
          >
            Search
          </Button>
        </div>
      </div>
    </div>
  );
}

export default PromptyInput;

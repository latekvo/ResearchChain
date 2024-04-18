"use client";
import React from "react";
import { Button, Input, Tab, Tabs } from "@nextui-org/react";
// import {SearchIcon} from "./SearchIcon";

function PromptyInput() {
  return (
    <div className="w-1/2 p-5 shadow-xl rounded-xl border border-opacity-15 border-gray-400 bg-black bg-opacity-55 z-10 flex flex-col justify-between">
      <Input
        variant="underlined"
        placeholder="Ask a question :)"
        color="secondary"
        size="lg"
        className="text-gray-300 px-3"
      />
      <div className="w-full mt-4 flex justify-between">
        <Tabs
          size="lg"
          aria-label="Options"
          variant="underlined"
          color="secondary"
        >
          <Tab key="news" title="News" />
          <Tab key="docs" title="Docs" />
          <Tab key="wiki" title="Wiki" />
        </Tabs>
        <div className="w-2/3 mr-3 flex flex-row-reverse">
          <Button
            size="lg"
            type="submit"
            color="default"
            variant="bordered"
            // endContent={<SearchIcon className="text-black/50 mb-0.5 dark:text-white/90 text-slate-400 pointer-events-none flex-shrink-0" />}
          >
            Search
          </Button>
        </div>
      </div>
    </div>
  );
}

export default PromptyInput;

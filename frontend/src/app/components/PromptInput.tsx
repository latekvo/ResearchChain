"use client";
import React from "react";
import { Button, Input, Tab, Tabs } from "@nextui-org/react";
// import {SearchIcon} from "./SearchIcon";

function PromptyInput() {
  return (
    <div className="w-1/2 h-1/4 p-5 rounded-2xl flex flex-col justify-between backdrop-blur-md bgcolor bg-black/50 drop-shadow-xl">
      <Input
        label="Topic of research:"
        isClearable
        radius="lg"
        classNames={{
          label: "text-black/50 dark:text-white/90 text-lg",
          input: [
            "text-2xl",
            "bg-transparent",
            "text-black/90 dark:text-white/90",
            "placeholder:text-default-700/50 dark:placeholder:text-white/60",
          ],
          innerWrapper: "bg-transparent",
          inputWrapper: [
            "self-center",
            "h-20",
            "shadow-xl",
            "bg-default-200/50",
            "dark:bg-default/60",
            "backdrop-blur-xl",
            "backdrop-saturate-200",
            "hover:bg-default-200/70",
            "dark:hover:bg-default/70",
            "group-data-[focused=true]:bg-default-200/70",
            "dark:group-data-[focused=true]:bg-default/60",
            "!cursor-text",
          ],
        }}
        placeholder="Type to search..."
      />
      <div className="w-full flex justify-between">
        <Tabs
          size="lg"
          aria-label="Options"
          classNames={{
            tabList:
              "shadow-xl dark:text-white/90 bg-default-200/70 dark:bg-default/70 backdrop-blur-xl backdrop-saturate-200",
            tabContent: "text-black/90 dark:text-white/90",
          }}
        >
          <Tab key="news" title="News" />
          <Tab key="docs" title="Docs" />
          <Tab key="wiki" title="Wiki" />
        </Tabs>
        <div className="w-2/3 flex flex-row-reverse">
          <Button
            size="lg"
            type="submit"
            className="ml-4 shadow-xl bg-default-200/70 dark:bg-default/70 backdrop-blur-xl backdrop-saturate-200 hover:bg-default-200/70 dark:hover:bg-default/70"
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

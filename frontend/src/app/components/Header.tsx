"use client";

import React from 'react';
import { Button, Tab, Tabs } from "@nextui-org/react";

const Header = () => {
  return (
    <div className="flex shadow-xl w-full border-b border-opacity-10 border-gray-400 bg-black bg-opacity-65 z-20 p-5 justify-between">
        <Tabs
          size="lg"
          aria-label="Options"
          variant="underlined"
          color="secondary"
          className='pl-6'
          classNames={{
            tab: "text-white",
          }}
        >
          <Tab className='text-xl px-4 ' key="add_task" title="Add task" />
          <Tab className='text-xl px-4' key="crawl_history" title="Crawl history" />
          <Tab className='text-xl px-4' key="summarize_history" title="Summarize history" />
        </Tabs>
      </div>
  );
};

export default Header;

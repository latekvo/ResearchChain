"use client";
import React, { Key, useState } from "react";
import { Button, Tab, Tabs, Textarea } from "@nextui-org/react";

interface FormValues {
  prompt: string;
  mode: string;
}

function PromptInput() {
  const [crawlActive, setCrawlActive] = useState(true);
  const [formValues, setFormValues] = useState<FormValues>({
    prompt: "",
    mode: "",
  });

  const onCrawlChange = (key: Key) => {
    if (key === "summarize") {
      setCrawlActive(false);
    } else {
      setCrawlActive(true);
    }
  };

  const addCrawl = () => {};
  const addSummarize = () => {};

  const onModeChange = (key: Key) => {
    setFormValues((prevValues) => ({
      ...prevValues,
      mode: String(key),
    }));
  };

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setFormValues((prevValues) => ({
      ...prevValues,
      [name]: value,
    }));
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (key === "summarize") {
      addSummarize();
    } else {
      addCrawl();
    }
    console.log(formValues);
  };

  return (
    <form className="w-3/5 flex-col" onSubmit={handleSubmit}>
      <Tabs
        size="md"
        aria-label="Options"
        color="default"
        variant="light"
        onSelectionChange={onCrawlChange}
        className="mb-3 shadow-xl rounded-xl border border-opacity-10 border-gray-400 bg-black bg-opacity-15 z-10 flex flex-col justify-between"
      >
        <Tab key="crawl" title="Crawl" />
        <Tab key="summarize" title="Summarize" />
      </Tabs>
      <div className="w-full p-5 shadow-xl rounded-xl border border-opacity-10 border-gray-400 bg-black bg-opacity-15 z-10 flex flex-col justify-between">
        <Textarea
          type="text"
          name="prompt"
          value={formValues.prompt}
          variant="underlined"
          placeholder="Ask a question :)"
          color="default"
          size="lg"
          minRows={1}
          onChange={handleChange}
          className="text-gray-300 px-3 text-large whitespace-normal"
        />
        <div className="w-full mt-4 flex justify-between">
          <Tabs
            size="lg"
            aria-label="Options"
            variant="underlined"
            color="default"
            isDisabled={!crawlActive}
            onSelectionChange={onModeChange}
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
    </form>
  );
}

export default PromptInput;

"use client";
import React, { Key, useState } from "react";
import { Button, Tab, Tabs, Textarea } from "@nextui-org/react";
import {
  UseMutationOptions,
  UseMutationResult,
  useMutation,
} from "react-query";
import { z } from "zod";

type FormValues = {
  prompt: string;
  mode: string;
};

type MutationResult = {
  success: boolean;
  message: string;
};

function PromptInput() {
  const [crawlActive, setCrawlActive] = useState(true);
  const [formValues, setFormValues] = useState<FormValues>({
    prompt: "",
    mode: "",
  });

  const FormData = z.object({
    prompt: z.string().min(1),
    mode: z.string(),
  });

  const onCrawlChange = (key: Key) => {
    if (key === "summarize") {
      setCrawlActive(false);
    } else {
      setCrawlActive(true);
    }
  };

  const addCrawl: UseMutationResult<MutationResult, unknown, FormValues> =
    useMutation(
      async (data: FormValues) => {
        const isValid = FormData.safeParse(data);
        if (!isValid.success) {
          throw new Error(isValid.error.message);
        }
        const response = await fetch("http://127.0.0.1:8000/crawl", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        });

        const result = await response.json();

        return result;
      },
      {
        onSuccess: (result) => {},
        onError: (error) => {},
      } as UseMutationOptions<MutationResult, unknown, FormValues>
    );

  const addSummarize: UseMutationResult<MutationResult, unknown, FormValues> =
    useMutation(
      async (data: FormValues) => {
        const isValid = FormData.safeParse(data);
        if (!isValid.success) {
          throw new Error(isValid.error.message);
        }
        const response = await fetch("http://127.0.0.1:8000/completion", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(data),
        });

        const result = await response.json();

        return result;
      },
      {
        onSuccess: (result) => {},
        onError: (error) => {},
      } as UseMutationOptions<MutationResult, unknown, FormValues>
    );

  const onModeChange = (key: Key) => {
    setFormValues((prevValues) => ({
      ...prevValues,
      mode: String(key),
    }));
  };

  const onPromptChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target;
    setFormValues((prevValues) => ({
      ...prevValues,
      [name]: value,
    }));
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (crawlActive) {
      addCrawl.mutate(formValues);
    } else {
      addSummarize.mutate(formValues);
    }
  };

  return (
    <form className="w-3/5 flex-col" onSubmit={handleSubmit}>
      <div className="w-full p-6 py-8 shadow-xl rounded-xl border border-opacity-10 border-gray-400 bg-black bg-opacity-15 z-10 flex flex-col justify-between">
        <Textarea
          type="text"
          name="prompt"
          value={formValues.prompt}
          variant="underlined"
          placeholder="Ask a question :)"
          color="default"
          size="lg"
          minRows={1}
          onChange={onPromptChange}
          className="text-gray-300 px-3 text-large whitespace-normal"
        />
        <Tabs
          size="md"
          aria-label="Options"
          color="primary"
          variant="light"
          onSelectionChange={onCrawlChange}
          className="mt-4 mb-2 shadow-xl  rounded-xl  bg-black bg-opacity-15 z-10 flex flex-col justify-between"
        >
          <Tab key="crawl" title="Crawl" />
          <Tab key="summarize" title="Summarize" />
        </Tabs>
        <div className="w-full mt-4 flex justify-between">
          <Tabs
            size="lg"
            aria-label="Options"
            variant="underlined"
            color="default"
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

import { useEffect, useRef } from "react";
import { Modal, ModalContent, ModalHeader, Button } from "@nextui-org/react";
import type { SummaryTask } from "../types/TaskType"; // Import SummaryTask
import { PiQueueDuotone } from "react-icons/pi";
import { MdDone } from "react-icons/md";
import { GrInProgress } from "react-icons/gr";
import { calculateElapsedTime } from "../hooks/calculateElapsedTime";

interface ExampleModalProps {
  isOpen: boolean;
  onClose: () => void;
  summaryTask: SummaryTask;
}

const ExampleModal: React.FC<ExampleModalProps> = ({
  isOpen,
  onClose,
  summaryTask,
}) => {
  const scrollableTargetRef = useRef<HTMLDivElement>(null);

  let status: string = "status";

  function getIconComponent(summaryTask: SummaryTask) {
    if (summaryTask.executing) {
      status = "Executing";
      return <GrInProgress color="#006fee" className="text-3xl my-auto " />;
    } else if (!summaryTask.executing && !summaryTask.completed) {
      status = "Queued";
      return (
        <PiQueueDuotone
          color="#ffff44bd"
          className="text-3xl my-auto  rounded-full"
        />
      );
    } else if (summaryTask.completed) {
      status = "Done";
      return (
        <MdDone color="#00f400a6" className="text-3xl my-auto  rounded-full" />
      );
    }
    return null;
  }

  return (
    <Modal
      size="3xl"
      backdrop="blur"
      scrollBehavior="inside"
      hideCloseButton={false}
      isOpen={isOpen}
      onClose={onClose}
      shouldBlockScroll={false}
      classNames={{
        backdrop: "top-0 left-0",
      }}
    >
      <ModalContent>
        <ModalHeader className="border-b-1 border-indigo-800 ">
          <div className="grid grid-cols-3 gap-40 items-center w-full py-2">
            <div className="flex justify-center">
              {getIconComponent(summaryTask)}
            </div>
            <div className="flex flex-col items-center">
              <p className="text-md text-center">Mode: {summaryTask.mode}</p>
              <p className="text-small text-default-500">Status: {status}</p>
            </div>
            <div className="flex flex-col items-center">
              <p className="text-md whitespace-pre-line text-center">
                {calculateElapsedTime(summaryTask.timestamp)}
              </p>
            </div>
          </div>
        </ModalHeader>
        <div className="display:contents">
          <div
            className="flex-1 overflow-y-auto px-6"
            ref={scrollableTargetRef}
          >
            <div className="grid grid-cols-3 py-4 gap-40 w-full">
              <div className="text-md text-center">
                <span className="text-xl">uuid</span>
                <span className="block">{summaryTask?.uuid}</span>
              </div>
              <div className="text-md text-center">
                Execution date
                <span className="block">
                  {calculateElapsedTime(summaryTask?.execution_date)}
                </span>
              </div>
              <div className="text-md text-center">
                Completion date
                <span className="block">
                  {calculateElapsedTime(summaryTask?.completion_date)}
                </span>
              </div>
            </div>
            <div className="pb-8">
              <div className="">
                <p className="pt-3 text-xl text-primary">Prompt</p>
                <p className="text-lg">{summaryTask?.prompt}</p>
              </div>
              <div className="">
                <p className="pt-3 text-xl text-primary">Completion result</p>
                <p className="text-lg">{summaryTask?.completion_result}</p>
              </div>
            </div>
          </div>
        </div>
      </ModalContent>
    </Modal>
  );
};

export default ExampleModal;

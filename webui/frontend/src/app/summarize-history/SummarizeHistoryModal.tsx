import { useEffect, useRef } from 'react';
import { Modal, ModalContent, ModalHeader, Button } from "@nextui-org/react";
import { SummaryTask } from '../types/TaskType'; // Import SummaryTask
import { PiQueueDuotone } from "react-icons/pi";
import { MdDone } from "react-icons/md";
import { GrInProgress } from "react-icons/gr";
import {calculateElapsedTime} from "../hooks/calculateElapsedTime"

interface ExampleModalProps {
  isOpen: boolean;
  onClose: () => void;
  summaryTask: SummaryTask
}

const ExampleModal: React.FC<ExampleModalProps> = ({ isOpen, onClose, summaryTask }) => {
  const scrollableTargetRef = useRef<HTMLDivElement>(null);

  let status:string = "status"

  function getIconComponent(summaryTask: SummaryTask) {
    if (summaryTask.executing) {
        status = "Executing"
        return <GrInProgress color="#006fee" className="text-3xl my-auto mr-6" />;
    } else if (!summaryTask.executing && !summaryTask.completed) {
        status = "Queued"
        return <PiQueueDuotone color="#ffff44bd" className="text-3xl my-auto mr-6 rounded-full" />;
    } else if (summaryTask.completed) {
        status ="Done"
        return <MdDone color="#00f400a6" className="text-3xl my-auto mr-6 rounded-full" />;
    }
    return null;
  }

  useEffect(() => {
    if (isOpen && scrollableTargetRef.current) {
      // Tutaj możesz umieścić dowolną logikę obsługi otwarcia modala, np. blokowanie scrolla
      return () => {
        // Tutaj możesz umieścić logikę czyszczenia, np. odblokowanie scrolla
      };
    }
  }, [isOpen]);

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
        backdrop: 'top-0 left-0',
      }}
    >
      <ModalContent>
        <ModalHeader>
        <div className="flex justify-between items-center w-full p-4">
        {getIconComponent(summaryTask)}
          <div className="flex flex-col">
            <p className="text-md text-center">Mode: {summaryTask.mode}</p>
            <p className="text-small text-default-500">Status: {status}</p>
          </div>
          <div>
            <p className="text-sm whitespace-pre-line text-center">{calculateElapsedTime(summaryTask.timestamp)}</p>
          </div>
        </div>
        </ModalHeader>
        <div className="display:contents">
          <div className="flex flex-1 flex-col gap-3 overflow-y-auto px-6" ref={scrollableTargetRef}>
            <div className="flex justify-between items-center w-full">
            <p>uuid: {summaryTask?.uuid}</p>
            <p>execution_date: {summaryTask?.execution_date}</p>
            <p>completion_date: {summaryTask?.completion_date}</p>
            </div>
            <div className='pb-8'>
            <p className='pt-3 text-xl text-primary'>Prompt</p> <p>{summaryTask?.prompt}</p>
            <p className='pt-3 text-xl text-primary'>Completion result</p>
            <p>{summaryTask?.completion_result}</p>
            </div>
          </div>
        </div>
      </ModalContent>
    </Modal>
  );
};

export default ExampleModal;

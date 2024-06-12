import { useEffect, useRef } from 'react';
import { Modal, ModalContent, ModalHeader, Button } from "@nextui-org/react";
import { SummaryTask } from '../types/TaskType'; // Import SummaryTask

interface ExampleModalProps {
  isOpen: boolean;
  onClose: () => void;
  summaryTask: SummaryTask
}

const ExampleModal: React.FC<ExampleModalProps> = ({ isOpen, onClose, summaryTask }) => {
  const scrollableTargetRef = useRef<HTMLDivElement>(null);

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
        <div className="display:contents">
          <ModalHeader className="flex flex-col gap-1">
            <div className="flex w-full items-center justify-between gap-2">
              <Button variant="light" isIconOnly onPress={onClose}>
                Close
              </Button>
            </div>
          </ModalHeader>
          <div className="flex flex-1 flex-col gap-3 overflow-y-auto px-6 py-2" ref={scrollableTargetRef}>
            <p>uuid: {summaryTask?.uuid}</p>
            <p>prompt: {summaryTask?.prompt}</p>
            <p>mode: {summaryTask?.mode}</p>
            <p>timestamp: {summaryTask?.timestamp}</p>
            <p>executing: {summaryTask?.executing.toString()}</p>
            <p>execution_date: {summaryTask?.execution_date}</p>
            <p>completed: {summaryTask?.completed.toString()}</p>
            <p>completion_date: {summaryTask?.completion_date}</p>
            <p>completion_result: {summaryTask?.completion_result}</p>
          </div>
        </div>
      </ModalContent>
    </Modal>
  );
};

export default ExampleModal;

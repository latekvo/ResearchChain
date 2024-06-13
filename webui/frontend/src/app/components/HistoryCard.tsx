import { Card, CardBody, CardHeader, Divider } from "@nextui-org/react";
import { PiQueueDuotone } from "react-icons/pi";
import { MdDone } from "react-icons/md";
import { GrInProgress } from "react-icons/gr";
import { calculateElapsedTime } from "../hooks/calculateElapsedTime";
import { CrawlTask } from "../types/TaskType";

type TaskCardProps = {
  item: CrawlTask;
  onClick?: (item: any) => void;
};

const HistoryCard: React.FC<TaskCardProps> = ({ item }) => {
    let status:string = "status"

  function getIconComponent(item: CrawlTask) {
    if (item.executing) {
        status = "Executing"
        return <GrInProgress color="#006fee" className="text-3xl my-auto mr-6" />;
    } else if (!item.executing && !item.completed) {
        status = "Queued"
        return <PiQueueDuotone color="#ffff44bd" className="text-3xl my-auto mr-6 rounded-full" />;
    } else if (item.completed) {
        status ="Done"
        return <MdDone color="#00f400a6" className="text-3xl my-auto mr-6 rounded-full" />;
    }
    return null;
  }

  return (
    <Card isBlurred={false} key={item.uuid} className="p-2 m-2 w-full h-5/6 mx-auto shadow-xl rounded-xl border border-opacity-15 border-gray-400 bg-black bg-opacity-25">
      <CardHeader className="p-1">
        <div className="flex justify-between items-center w-full">
        {getIconComponent(item)}
          <div className="flex flex-col">
            <p className="text-md text-center">Mode: {item.mode}</p>
            <p className="text-small text-default-500">Status: {status}</p>
          </div>
          <div>
            <p className="text-sm whitespace-pre-line text-center">{calculateElapsedTime(item.timestamp)}</p>
          </div>
        </div>
      </CardHeader>
      <Divider />
      <CardBody className="h-14 p-2">
        <p className="text-sm text-default-600">{item.prompt}</p>
      </CardBody>
    </Card>
  );
};

export default HistoryCard;

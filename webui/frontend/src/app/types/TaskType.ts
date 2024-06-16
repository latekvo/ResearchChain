export interface Task {
  uuid: string;
  prompt: string;
  mode: string;
  timestamp: number;
  executing: boolean;
  execution_date: number;
  completed: boolean;
  completion_date: number;
}

export interface CrawlTask extends Task {}

export interface SummaryTask extends Task {
  completion_result: string;
}

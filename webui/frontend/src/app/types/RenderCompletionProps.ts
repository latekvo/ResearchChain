export interface RenderCompletionProps {
  executing: boolean;
  completion_result: string | undefined;
  handleClose: () => void;
}

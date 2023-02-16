export interface GetSolutionData {
  solution_id: number;
  solution_user: number;
  solution_exercise: number;
  solution_date: number;
  solution_duration: number;
  solution_pending: boolean;
  solution_correct: boolean;
  solution_content: object;
}

export interface GetSolutionMeta {
  next_page: number;
  next_url: number;
  page_size: number;
  pages: number;
  prev_page: number;
  prev_url: number;
  total: number;
}

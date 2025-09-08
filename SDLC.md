# Scholar Grid

## Requirements
1. The user should be able to add paper (either upload or via url)
2. The user should be able to create a new grid by selecting papers and entering questions
3. The user should be able to edit the grid, i.e. add/remove papers and questions

## Planning
1. Init frontend and backend
2. Setup paper ingestion and storage
3. Setup paper parsing (PDF -> md)
4. Library management (Paper crud)
5. Setup LLMs
6. Create LLM parsing pipeline
7. Grid creation (w/o LLM)
8. With LLM
9. Grid editing

## UI

## Tech stack
1. Backend: FastAPI
2. Database: SQLite
3. File storage: Localstorage
4. PDF processing: Marker and pymupdf4llm
5. LLM: Free big (>100B params) llms from OpenRouter
6. Frontend: NextJs
7. UI: TailwindCSS
8. Tables: AG grid

## Flow
1. User uploads papers -> Creates new grid -> selects papers and enters questions -> saves grid
2. User edits grid -> adds/removes papers and questions -> saves grid

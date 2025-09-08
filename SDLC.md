# Scholar Grid

## Requirements
1. The user should be able to add paper (either upload or via url)
2. The user should be able to create a new grid by selecting papers and entering questions
3. The user should be able to edit the grid, i.e. add/remove papers and questions

## Planning
1. [X] Init frontend and backend
2. [X] Setup paper ingestion and storage
    > __TODO__: Title and author extraction is left
3. [X] Setup paper parsing (PDF -> md)
    > __TODO__: Add more advanced models (marker)
4. [X] Setup LLMs
5. [X] Create LLM parsing pipeline
6. [X] Grid creation (w/o LLM)
7. [X] With LLM
8. Grid editing
9. Setup Alembic
10. Frontend...

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

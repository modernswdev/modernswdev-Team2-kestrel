# PawLink UX & Presentation Ideas (Elizabeth)

## Potential UI / Feature Improvements
- **Dog Photo Upload:** Allow owners to upload a profile picture for their dog.
- **Owner Name on Match Cards:** Display the matched dog's owner username alongside the dog's profile.
- **Grid Layout for Matches:** Arrange match details cleanly so multiple matches display side-by-side in a responsive grid instead of a single vertical column.
- **Select / Contact a Match:** Add action buttons directly on match cards to message an owner (#28) or request a park meetup (#27).
- **City & State Display:** Resolve ZIP codes to actual city/state names (using the existing `app/zip_codes.csv` dataset) in addition to showing distance in miles.

## Notes for Nov 30 Presentation
- Highlight the working end-to-end MVP flow: Register -> Log In -> Create Dog Profile -> Browse Ranked Matches.
- Highlight engineering practices: 43 automated `pytest` tests, GitHub Actions CI enforcement, protected `main` branch with peer-reviewed PRs, and Haversine distance + weighted compatibility scoring.
- Present the list above as our **Next Iteration / Future Roadmap** slide.
- **Align Scoring Formula with Spec (`docs/compatibility_computation.md`):** Update `app/compatibility.py` (and `tests/test_compatibility.py`) from the simplified 3-tier subtraction penalty to the original 5-tier division formula (`÷ 1.0`, `÷ 1.5`, `÷ 2.0`, `÷ 2.5`, `÷ 3.0`) so long-distance matches scale down proportionally.
- **Align Scoring Formula with Spec (`docs/compatibility_computation.md`):** Update `app/compatibility.py` (and `tests/test_compatibility.py`) from the simplified 3-tier subtraction penalty to the original 5-tier division formula (`÷ 1.0`, `÷ 1.5`, `÷ 2.0`, `÷ 2.5`, `÷ 3.0`) so long-distance matches scale down proportionally.

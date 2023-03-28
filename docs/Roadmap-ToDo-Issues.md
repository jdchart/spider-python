# Roadmap & To-Do:

## Roadmap
- [ ] Functionality for quickly following a project on local machine(s). For example, an artist may track their work at certain points in the process, a programmer may track the development of their code. This would mean having a web based on a folder on a machine, and havign functionality for scanning the folder, assessing changes, adding modification times to the changed elements or add new elemnts, on remove old content (set it's end coverage time).
- [ ] GUI for construction, database navigation, validation of operations.
    - Also explore other validation methods.

## To-Do
- [ ] General refactor
    - Add type checking, checking if None (espicially for finding elements).
    - Better unit testing.
- [ ] Langaugages and translations.
    - Implement languaged fields for modified dublin core.
    - Update tags on language change (and check various updates on content changes).
    - Langugae removal fucntionality. Remove content when language removed?
- [ ] Check: searching probably doesnt work now with language overhaul.
- [ ] General element removal routines.
- [ ] Colleciton creation: add content straignt from creation method.
- [ ] Create a new web from collections.
- [ ] Network creation:
    - Make edges between nested nodes.
    - Mis-match between giving a collection and the defaults being lists !
- [ ] MR Conversion:
    - At the moment we only take the first source/target region for edges.
    - Copy media for nested nodes.
    - Need to unhard code overlaying.
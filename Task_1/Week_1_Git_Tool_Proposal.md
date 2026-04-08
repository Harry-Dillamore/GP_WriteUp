# Git Management Tool Proposal

## Proposed Tool: Anchorpoint

### 1. Overview & Objective
**Goal:** Integrate **Anchorpoint**, an existing Git client specifically designed for game development and Unreal Engine, to handle version control, Git LFS (Large File Storage), and binary file locking for the *Greedy Piggies* repository.

### 2. Intended Users & Target Platform
- **Intended Users:** Level Designers, 3D Artists, Animators, and Developers.
- **Target Platform:** Desktop Client (Windows/macOS) running alongside Unreal Engine.

### 3. Key Data and File Formats
- **.uasset & .umap:** Unreal's proprietary binary file formats. These are mission-critical because they cannot be merged line-by-line; conflicts require one person's work to be overwritten.
- **Git LFS Locks:** Anchorpoint communicates with the Git remote server to read and write LFS lock states seamlessly.

### 4. Implementation Steps
1. **Onboard the Team to Anchorpoint:**
   - Distribute Anchorpoint to the team as the primary Git client, replacing complex command-line interfaces or generic Git UI clients (like SourceTree/GitHub Desktop).
2. **Configure Git LFS and Locking Rules:**
   - Link the current Git repository to the platform. Configure the LFS tracking rules via the UI to ensure `.uasset` and `.umap` files are robustly tracked.
3. **Establish a Lock-Before-Edit Workflow:**
   - Train artists and designers to click the prominent "Lock" button in the Anchorpoint UI on the specific assets they intend to work on. The UI visually displays lock indicators with the profile avatars of users who currently own those locks. 
4. **Automate Syncing & Unlocking:**
   - Utilize Anchorpoint's visual timeline to effortlessly push and pull changes. Upon committing modifying local files, Anchorpoint can automatically release the locks, preventing bottlenecks where someone forgets to clear their lock at the end of the day.

### 5. Expected Value to Production
By adopting an existing, purpose-built tool like Anchorpoint instead of building a custom solution from scratch, the team can instantly alleviate Git repository conflicts:
- **Zero Development Overhead:** Allows you (the Lead Developer) to focus strictly on the *Greedy Piggies* core gameplay loop and card tool rather than sinking weeks into building and maintaining a custom in-editor Git utility.
- **Eliminates Lost Work:** Anchorpoint’s highly legible UI clearly shows who has locked an Unreal Engine asset, preventing two people from editing the same file concurrently and forcefully overwriting each other’s binary files.
- **Lowers the Barrier to Version Control:** It strips away intimidating Git jargon for artists, replacing complex branching workflows with intuitive visual timelines and file systems. This ensures that designers and animators can comfortably contribute to the Git repo without the constant fear of breaking the build.

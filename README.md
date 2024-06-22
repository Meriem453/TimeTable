This code generates a timetable for multiple groups, ensuring various constraints are met. It schedules lectures and practical sessions while avoiding conflicts, synchronizing lectures, and designating free slots.
<h2>Tools Used</h2>
    <ul>
        <li><strong>Constraints python package</strong>: Includes custom constraints for lectures and TD sessions, as well as built-in constraints like <code>AllDifferentConstraint</code>.</li>
        <li><strong>Backtracking Algorithm</strong>: Utilized by the <code>constraint</code> library for finding solutions to the CSP.</li>
        <li><strong>Arc Consistency (AC3)</strong>: Enforced to reduce the search space and improve efficiency, although not explicitly shown in the given code.</li>
    </ul>

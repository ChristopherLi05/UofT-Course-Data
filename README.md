# U of T Course Data

This is a repository containing data regarding U of T course data. There currently are 3 sources of information:

- U of T course evals (`course_evals.py`)
- Rate my Prof general ratings (`rate_my_prof.py`)
- U of T timetable data (`https://github.com/ICPRplshelp/Enrollment-Data/tree/master`)

All data is updated as of 2/20/2026

---

# Dataset Descriptions

## Course Evals

Description: Scraped data from U of T course evals

File location: `data/course_evals.csv`

Dataset Description:

| Column Name      | Description                                                                                                                            |
|------------------|----------------------------------------------------------------------------------------------------------------------------------------|
| dept             | 3 letter code used to describe the department                                                                                          |
| division         | U of T division, only contains `ARTSC` (artsci)                                                                                        |
| course           | Full course name                                                                                                                       |
| last_name        | Last name of the professor teaching the course                                                                                         |
| first_name       | First name of the professor teaching the course                                                                                        |
| term             | Term that the course was taken in (`Fall`, `Winter`, `Summer`); year courses default to `Winter`                                       |
| year             | Year that the course was taken in                                                                                                      |
| INS1             | "I found this course was intellectually stimulating"                                                                                   |
| INS2             | "The course provided me with a deeper understanding of the subject matter"                                                             |
| INS3             | "The instructor created a course atmosphere that was conducive to my learning."                                                        |
| INS4             | "Course projects, assignments, tests and/or exams improved my understanding of the course material."                                   |
| INS5             | "Course projects, assignments, tests and/or exams provided opportunity for me to demonstrate an understanding of the course material." |
| INS6             | "Overall, the quality of my learning experience in this course was:"                                                                   |
| ARTSC1           | "The instructor generated enthusiasm for learning in the course."                                                                      |
| ARTSC2           | "Compared to other courses, the workload for this course was…"                                                                         |
| ARTSC3           | "I would recommend this course to other students."                                                                                     |
| number_invited   | Number of people invited to take the eval                                                                                              |
| number_responses | Number of people who responded                                                                                                         |
| course_code      | Cleaned course code                                                                                                                    |

## Rate My Prof

Description: Scraped data from Rate My Prof

File location: `data/ratemyprof.csv`

Dataset Description:

| Column Name           | Description                                                  |
|-----------------------|--------------------------------------------------------------|
| id                    | Internal ID used by Rate My Professors                       |
| legacyId              | Legacy identifier used by older Rate My Professors systems   |
| firstName             | First name of the professor                                  |
| lastName              | Last name of the professor                                   |
| avgRating             | Average rating (from 1 to 5)                                 |
| numRatings            | Number of ratings for the professor                          |
| wouldTakeAgainPercent | Average percentage of people who would take the course again |
| avgDifficulty         | Average difficulty (from 1 to 5)                             |
| department            | Department the professor is in                               |

## Rate My Prof

Description: Scraped course data from Rate My Prof

File location: `data/ratings.csv`

Dataset Description

| Column Name         | Description                                         |
|---------------------|-----------------------------------------------------|
| prof_id             | Internal id used by Rate My Professors              |
| comment             | Comment associated with the review                  |
| date                | YYYY-MM-DD HH-MM-SS +0000 UTC                       |
| class               | Course code for the class                           |
| helpfulRating       | How helpful students found the course (from 1 to 5) |
| clarityRating       | How clear the course was (from 1 to 5)              |
| difficultyRating    | How difficult the course was (from 1 to 5)          |
| attendenceMandatory | Whether attendence was mandatory or not             |
| Would take again    | `1.0` for Yes, `null` or `0.0` for No               |
| Grade               | The students' self reported grade                   |
| Textbook Use        | ???                                                 |
| isForOnlineClass    | True/False                                          |
| isForCredit         | True/False                                          |
| ratingTags          | `--` delimited list of rating tags, up to 3         |

## Prof Mapping

Description: A mapping of course eval prof names to their corresponding rate my prof ids; some profs may have multiple
due to fuzzy matching used

File location: `data/prof_mappings.json`

Dataset Description: Json Dict containing `"FIRST LAST": [RMP_IDS]`

## Valid Courses

Description: All valid course ids to be used in `Enrollment-Data`

File location: `data/courses.json`

Dataset Description: Json array containing course codes of the form "SLA337H1"

## Course Enrolment Data

Description: TTB enrolment data scraped by ICPRplshelp

File location: `Enrollment-Data/*`

Dataset Description: Files are located in `Enrollment-Data/YYYYT/COURSE_CODE.json`

```yaml
{
  "code": str,  # Course code
  "faculty": str,  # Course faculty
  "meetings": [
    {
      "createdAt": int,  # Time course was created
      "delivery": str,  # Delivery type, INPER or something else
      "enrollmentCap": int,  # Max amount of students that can enrol in the section
      "enrollmentCapComplex": { ... },  # Cap detailed
      "enrollmentLogs": [ int ],  # Enrolment per timestep
      "instructorLog": { ... },  # Instructor log
      "instructors": [
        {
          "firstName": str,  # Professor first name
          "lastName": str  # Professor last name
        }
      ],
      "isCancelled": bool,  # Whether the course was cancelled
      "meetingNumber": str  # Section id in the form of "LEC0101"
    }
  ],
  "timeIntervals": [ int ],  # Updated timestamps
  "title": str  # Course title
}
```
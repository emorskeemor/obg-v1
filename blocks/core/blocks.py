
def get_subject_count(data, options):
    subjects = dict.fromkeys(options, 0)
    for options in data:
        for subject in options:
            if subject:
                count = subjects.get(subject)
                if count is not None:
                    count += 1
                subjects.update({subject:count})
    return {k:v for k, v in sorted(subjects.items(), key=lambda x:x[1], reverse=True)}




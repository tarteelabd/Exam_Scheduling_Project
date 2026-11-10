# Exam_Scheduling_Project

## جدولة الامتحانات باستخدام تلوين الرسوم

**BIA601 — Intelligent Algorithms / الخوارزميات الذكية — الوظيفة الثانية (F25)**

مشروع جدولة امتحانات يقلّل عدد الفترات مع منع تعارض طالب في امتحانين بنفس الفترة. نقارن خوارزمية جينية (GA) وأسراب الجسيمات (PSO) ومستعمرة النمل (ACO) مع تلوين جشع ومرجع دقيق للحالات الصغيرة وحد أدنى لبقية الأحجام. البيانات مولّدة وليست سجلات جامعة فعلية.

Exam scheduling as graph coloring: assign each exam a period so that students never sit two exams at once, using GA, PSO, and ACO written from scratch.

## فريق العمل — Group 1

| العضو | GitHub | المسؤولية | القضية |
|---|---|---|---|
| ترتيل صالح | [tarteelabd](https://github.com/tarteelabd) | التكامل النهائي والتوثيق | [#9](https://github.com/tarteelabd/Exam_Scheduling_Project/issues/9) |
| ايهاب علوزي | [EHAB621](https://github.com/EHAB621) | نموذج المسألة والقيود والمراجع | [#1](https://github.com/tarteelabd/Exam_Scheduling_Project/issues/1) |
| آية العرنوس | [cafsgsvwv-design](https://github.com/cafsgsvwv-design) | خوارزمية GA | [#2](https://github.com/tarteelabd/Exam_Scheduling_Project/issues/2) |
| ربا صقر | [ruba-saqr](https://github.com/ruba-saqr) | خوارزمية PSO | [#3](https://github.com/tarteelabd/Exam_Scheduling_Project/issues/3) |
| محمد الجاويش | [algawishmohamed757-svg](https://github.com/algawishmohamed757-svg) | خوارزمية ACO | [#4](https://github.com/tarteelabd/Exam_Scheduling_Project/issues/4) |
| ايناس رحال | [einasryd](https://github.com/einasryd) | منصة التجارب والنتائج | [#5](https://github.com/tarteelabd/Exam_Scheduling_Project/issues/5) |
| هدى فوال | [HudaFawal](https://github.com/HudaFawal) | التحقق من القيود والحلول، والتقرير النهائي | [#6](https://github.com/tarteelabd/Exam_Scheduling_Project/issues/6) |
| راما بعيون | [ramaBayon](https://github.com/ramaBayon) | مخرجات التجارب ولوحة العرض | [#7](https://github.com/tarteelabd/Exam_Scheduling_Project/issues/7) |
| abdalwadood867-glitch | [abdalwadood867-glitch](https://github.com/abdalwadood867-glitch) | كتابة التقرير النهائي وتوثيق مهام الأعضاء | [#8](https://github.com/tarteelabd/Exam_Scheduling_Project/issues/8) |

مساهمة كل عضو موثّقة في التقرير (`Report.docx`) وفي تاريخ المستودع. الفريق تسعة أعضاء (ضمن شرط المقرر: 6 إلى 9).

## التشغيل

Python 3.12 أو أحدث، من مجلد `project`:

```text
python -m pip install -r requirements.txt
python experiment.py
python verify.py
```

تجربة قصيرة تكتب في مجلد مستقل:

```text
python experiment.py --runs 2 --output ../trial_results
python verify.py --results ../trial_results
```

إعادة أول تشغيلة لكل خوارزمية ولكل مسألة، مع فحص سجل التقارب:

```text
python verify.py --rerun
```

التفاصيل التقنية موجودة في [`project/README.md`](project/README.md).

## النتائج والعرض

- التقرير: [`Report.docx`](Report.docx)
- لوحة النتائج التفاعلية: افتح [`index.html`](index.html) في المتصفح (ملف مستقل، لا يحتاج تشغيل خادم).
  لعرض الجداول والرسوم بعد التجربة الكاملة يكفي فتح الملف محلياً. الصفحة لا تنفّذ خوارزميات Python.
- بعد إعادة التجارب يمكن تحديث بيانات الصفحة عبر:

```text
python export_web_data.py
```

- مخرجات التجارب والرسوم: [`project/results/`](project/results/)

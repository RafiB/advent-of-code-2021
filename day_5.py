from collections import defaultdict

import attr


TEST_INPUT = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""


PUZZLE_INPUT = """657,934 -> 657,926
130,34 -> 570,474
478,716 -> 226,464
861,110 -> 861,167
448,831 -> 370,831
75,738 -> 390,738
26,880 -> 864,42
965,658 -> 527,220
208,381 -> 80,381
523,475 -> 807,475
219,69 -> 219,434
793,538 -> 534,797
754,602 -> 754,148
443,327 -> 443,611
606,395 -> 546,395
980,56 -> 51,985
619,325 -> 354,325
342,123 -> 819,600
290,533 -> 374,533
598,77 -> 598,75
605,302 -> 605,636
97,981 -> 692,386
278,779 -> 278,800
661,377 -> 661,10
726,108 -> 518,316
271,883 -> 271,50
382,271 -> 606,271
963,358 -> 891,286
496,880 -> 496,855
211,142 -> 211,49
841,866 -> 260,285
841,849 -> 173,181
927,326 -> 391,862
396,558 -> 459,558
753,183 -> 953,183
941,698 -> 941,407
347,612 -> 347,476
18,340 -> 18,612
140,299 -> 797,956
714,907 -> 714,228
966,155 -> 194,927
769,674 -> 712,674
644,675 -> 948,979
703,872 -> 812,763
26,629 -> 120,535
844,738 -> 844,253
798,133 -> 798,795
27,318 -> 288,57
38,545 -> 872,545
827,351 -> 195,983
818,45 -> 21,842
257,559 -> 626,928
145,925 -> 886,184
83,618 -> 590,111
326,243 -> 53,243
489,278 -> 526,278
783,693 -> 783,525
495,636 -> 495,585
374,716 -> 215,557
839,536 -> 839,966
850,468 -> 955,468
55,799 -> 55,447
472,722 -> 296,898
390,731 -> 120,461
405,493 -> 208,296
807,42 -> 56,793
476,327 -> 655,327
24,965 -> 967,22
776,211 -> 776,850
489,20 -> 822,20
630,740 -> 871,499
743,493 -> 283,953
62,429 -> 62,720
806,270 -> 806,332
550,154 -> 107,597
71,713 -> 533,251
620,575 -> 620,156
726,829 -> 143,246
944,553 -> 468,553
185,582 -> 185,468
845,266 -> 212,899
654,97 -> 265,486
726,609 -> 726,147
631,76 -> 860,76
835,24 -> 928,24
712,719 -> 74,81
616,478 -> 616,117
903,226 -> 903,577
440,699 -> 136,395
215,705 -> 890,30
20,24 -> 981,985
102,144 -> 850,892
695,967 -> 582,967
219,284 -> 219,388
359,833 -> 665,833
389,55 -> 305,55
59,32 -> 957,930
815,198 -> 64,949
699,540 -> 717,558
215,682 -> 182,682
805,489 -> 328,489
43,546 -> 578,546
489,181 -> 489,363
266,391 -> 266,582
863,368 -> 448,368
83,236 -> 83,487
874,875 -> 874,413
799,90 -> 799,802
253,29 -> 253,905
136,446 -> 435,745
830,534 -> 550,534
183,785 -> 107,785
81,517 -> 159,517
359,941 -> 359,560
71,546 -> 948,546
596,811 -> 596,791
255,960 -> 255,159
788,15 -> 788,682
240,55 -> 240,244
51,423 -> 137,423
504,418 -> 809,723
131,842 -> 914,59
727,790 -> 82,145
281,509 -> 841,509
797,807 -> 834,807
333,499 -> 790,499
215,328 -> 215,139
500,898 -> 500,862
75,217 -> 777,919
17,264 -> 17,446
852,755 -> 150,755
865,186 -> 385,186
158,192 -> 158,733
196,261 -> 196,128
989,960 -> 131,102
807,393 -> 807,153
507,579 -> 507,764
468,76 -> 535,76
381,357 -> 659,357
794,277 -> 749,277
51,152 -> 546,647
797,959 -> 458,959
82,156 -> 967,156
261,624 -> 460,624
597,53 -> 197,53
153,507 -> 411,765
305,717 -> 768,717
344,954 -> 344,217
194,432 -> 545,432
346,46 -> 557,46
685,599 -> 685,312
49,719 -> 49,631
499,668 -> 304,863
262,405 -> 554,405
87,64 -> 295,64
859,675 -> 74,675
663,776 -> 99,212
232,189 -> 232,904
777,276 -> 703,276
704,492 -> 86,492
142,736 -> 514,364
418,611 -> 224,417
602,571 -> 602,424
152,603 -> 248,603
915,673 -> 143,673
538,32 -> 128,32
975,885 -> 975,344
870,511 -> 870,756
330,798 -> 46,798
440,195 -> 587,195
739,237 -> 568,66
54,838 -> 196,980
370,556 -> 47,556
124,575 -> 748,575
261,283 -> 880,902
784,91 -> 426,449
764,670 -> 148,670
32,51 -> 967,986
807,906 -> 10,906
470,488 -> 579,597
274,649 -> 285,649
221,540 -> 221,94
914,957 -> 914,510
879,825 -> 145,91
438,833 -> 438,775
191,844 -> 911,124
145,763 -> 595,763
504,81 -> 622,199
834,206 -> 834,704
908,308 -> 815,308
929,567 -> 929,322
805,50 -> 620,235
36,409 -> 133,312
345,375 -> 19,701
468,948 -> 468,108
109,547 -> 446,547
929,916 -> 69,56
927,857 -> 318,248
833,948 -> 833,61
559,787 -> 559,982
293,825 -> 293,775
508,744 -> 545,744
827,713 -> 753,639
88,775 -> 555,775
523,812 -> 684,812
307,142 -> 307,265
636,40 -> 355,321
891,875 -> 891,25
301,423 -> 712,12
922,187 -> 219,890
45,447 -> 230,262
114,568 -> 233,687
573,398 -> 677,398
334,101 -> 324,101
957,277 -> 957,652
943,834 -> 610,834
523,632 -> 523,379
958,361 -> 90,361
408,824 -> 380,824
647,314 -> 647,449
747,83 -> 59,83
776,104 -> 937,104
16,984 -> 989,11
362,581 -> 362,226
72,962 -> 940,94
319,877 -> 319,122
310,206 -> 986,882
794,877 -> 267,877
855,58 -> 976,58
699,971 -> 598,971
162,556 -> 162,440
494,859 -> 494,255
794,210 -> 142,862
275,510 -> 548,510
739,592 -> 739,793
376,985 -> 376,990
755,264 -> 280,739
187,34 -> 187,688
770,827 -> 770,548
10,68 -> 913,971
571,427 -> 571,944
153,211 -> 153,560
976,972 -> 55,51
103,611 -> 674,40
95,972 -> 924,143
929,94 -> 38,985
777,330 -> 60,330
312,430 -> 312,326
549,433 -> 269,433
477,267 -> 477,403
598,375 -> 19,375
512,799 -> 512,831
348,700 -> 348,43
165,97 -> 63,199
38,835 -> 38,828
282,334 -> 282,909
14,891 -> 390,515
930,657 -> 334,61
630,341 -> 630,85
671,464 -> 319,112
949,340 -> 894,285
663,916 -> 245,916
114,395 -> 286,223
335,804 -> 529,804
567,338 -> 14,891
623,705 -> 379,949
82,864 -> 545,401
932,128 -> 932,134
291,294 -> 291,101
739,765 -> 739,757
460,94 -> 892,94
375,673 -> 367,681
81,831 -> 90,831
890,402 -> 890,138
775,547 -> 790,547
49,927 -> 966,10
23,116 -> 257,116
923,75 -> 18,980
63,986 -> 687,362
369,844 -> 357,844
790,188 -> 644,188
557,282 -> 557,669
861,173 -> 390,644
480,529 -> 893,529
32,960 -> 830,162
368,725 -> 368,40
502,600 -> 701,600
63,977 -> 873,167
463,518 -> 788,193
738,406 -> 324,406
162,931 -> 822,931
377,487 -> 707,817
610,319 -> 901,319
586,658 -> 690,658
25,288 -> 53,288
760,602 -> 760,628
294,62 -> 951,62
222,773 -> 661,334
151,483 -> 646,483
272,852 -> 317,852
557,906 -> 503,960
736,445 -> 736,703
241,376 -> 241,692
835,41 -> 835,369
987,743 -> 987,210
42,700 -> 42,244
646,136 -> 646,440
544,751 -> 404,751
295,651 -> 295,805
687,878 -> 113,878
290,142 -> 604,142
579,920 -> 579,807
12,985 -> 987,10
919,940 -> 919,808
770,143 -> 770,832
114,76 -> 962,76
876,882 -> 428,434
861,139 -> 861,320
888,59 -> 888,39
629,823 -> 707,823
296,598 -> 296,305
61,54 -> 578,54
864,58 -> 253,58
71,861 -> 306,861
682,181 -> 326,537
307,418 -> 307,910
810,251 -> 810,431
151,836 -> 602,385
954,987 -> 243,276
724,272 -> 350,646
134,295 -> 434,295
178,235 -> 802,859
832,688 -> 832,573
165,334 -> 165,378
816,26 -> 114,728
668,192 -> 540,192
730,341 -> 969,341
951,169 -> 286,834
647,115 -> 886,115
664,288 -> 507,131
609,362 -> 609,295
747,479 -> 287,19
350,967 -> 350,725
117,383 -> 311,383
871,124 -> 292,124
654,271 -> 547,271
525,773 -> 345,953
401,670 -> 610,670
930,196 -> 301,825
336,37 -> 961,662
714,212 -> 714,667
454,848 -> 454,107
587,390 -> 587,577
530,437 -> 542,437
304,229 -> 517,229
340,571 -> 766,571
727,941 -> 138,352
831,325 -> 11,325
241,294 -> 403,456
788,658 -> 788,126
337,360 -> 337,589
799,402 -> 342,402
530,820 -> 530,319
982,27 -> 20,989
923,936 -> 923,721
581,395 -> 64,912
61,509 -> 61,827
989,580 -> 610,580
477,592 -> 219,592
296,775 -> 296,58
204,12 -> 204,457
190,171 -> 190,673
939,200 -> 939,457
472,282 -> 472,631
983,331 -> 734,331
365,609 -> 365,817
640,698 -> 145,698
103,618 -> 549,618
454,319 -> 454,346
650,815 -> 381,546
624,603 -> 507,603
966,445 -> 723,445
763,129 -> 763,784
695,145 -> 695,511
498,84 -> 435,147
188,716 -> 967,716
810,446 -> 810,924
731,483 -> 731,51
307,783 -> 307,533
15,956 -> 956,15
192,210 -> 882,210
303,173 -> 38,438
769,952 -> 769,863
135,781 -> 405,781
494,436 -> 494,892
705,394 -> 714,394
164,37 -> 164,633
813,232 -> 813,620
227,906 -> 222,906
542,432 -> 414,432
549,858 -> 88,397
200,101 -> 958,859
235,565 -> 469,331
492,871 -> 503,882
704,398 -> 869,563
450,736 -> 746,736
420,706 -> 420,635
717,493 -> 686,524
187,554 -> 717,24
31,851 -> 315,851
800,230 -> 466,230
226,324 -> 226,614
937,927 -> 937,798
143,26 -> 534,417
952,344 -> 12,344
181,361 -> 782,361
925,906 -> 415,396
685,944 -> 470,944
200,627 -> 290,627
728,285 -> 728,326
271,864 -> 271,34
802,558 -> 207,558
963,26 -> 84,905
504,60 -> 529,60
840,292 -> 180,292
914,272 -> 914,330
82,107 -> 925,950
33,245 -> 33,134
463,663 -> 463,82
27,305 -> 27,675
276,894 -> 891,279
746,325 -> 746,948
249,657 -> 341,749
530,848 -> 28,346
798,617 -> 798,609
119,767 -> 312,767
80,18 -> 674,18
723,374 -> 583,374
582,985 -> 239,642
217,765 -> 217,395
811,159 -> 609,159
689,896 -> 501,896
562,881 -> 562,96
244,621 -> 629,621
277,379 -> 277,287
856,153 -> 20,153
518,228 -> 518,898
230,789 -> 243,789
534,335 -> 534,592
240,790 -> 413,617
768,615 -> 768,560
773,101 -> 912,101
252,571 -> 767,56
370,595 -> 681,906
565,176 -> 565,318
750,465 -> 750,724
979,130 -> 120,989
160,153 -> 160,785
610,222 -> 610,191
873,124 -> 130,867
519,593 -> 519,32
525,947 -> 525,562
50,292 -> 291,533
558,927 -> 960,525
536,694 -> 249,981
954,896 -> 277,896
732,202 -> 732,288
447,989 -> 541,895
890,754 -> 367,231
368,89 -> 564,285
588,100 -> 588,156
282,313 -> 943,974
16,792 -> 495,792
111,591 -> 111,493
57,713 -> 685,85
676,632 -> 676,575
560,708 -> 560,602
489,288 -> 489,404
904,515 -> 443,54
70,977 -> 985,62
11,119 -> 11,403
215,859 -> 937,137
78,469 -> 110,437
747,605 -> 747,369
847,598 -> 847,299
742,695 -> 159,112
986,370 -> 986,460
631,900 -> 771,760
228,406 -> 683,861
189,639 -> 61,639
221,650 -> 820,650
558,569 -> 834,845
655,533 -> 558,630
967,921 -> 967,169
230,308 -> 429,308
873,762 -> 873,528
412,151 -> 412,538
881,587 -> 881,21
941,45 -> 26,960
377,126 -> 700,126"""

@attr.s()
class Coord(object):
    x = attr.ib()
    y = attr.ib()


@attr.s()
class Line(object):
    start = attr.ib()
    end = attr.ib()


def solve(lines_str):
    lines = []

    for line_desc in lines_str.split("\n"):
        start, end = line_desc.split(" -> ")
        start_x, start_y = start.split(",")
        end_x, end_y = end.split(",")
        lines.append(
            Line(
                start=Coord(x=int(start_x), y=int(start_y)),
                end=Coord(x=int(end_x), y=int(end_y)),
            )
        )

    points = defaultdict(int)

    for line in lines:
        if line.start.x == line.end.x:
            start = min(line.start.y, line.end.y)
            end = max(line.start.y, line.end.y)
            for y in range(start, end + 1):
                points[(line.start.x, y)] += 1
        elif line.start.y == line.end.y:
            start = min(line.start.x, line.end.x)
            end = max(line.start.x, line.end.x)
            for x in range(start, end + 1):
                points[(x, line.start.y)] += 1
        else:
            start = line.start.x
            end = line.end.x
            y = line.start.y
            if line.start.x < line.end.x:
                if line.start.y < line.end.y:
                    dir_ = (1, 1)
                else:
                    dir_ = (1, -1)
            else:
                if line.start.y < line.end.y:
                    dir_ = (-1, 1)
                else:
                    dir_ = (-1, -1)

            while start != end + dir_[0]:
                points[(start, y)] += 1
                start += dir_[0]
                y += dir_[1]

    n = 0
    for point, count in points.items():
        if count >= 2:
            n += 1

    return n


if __name__ == "__main__":
    assert solve(TEST_INPUT) == 12
    print(solve(PUZZLE_INPUT))

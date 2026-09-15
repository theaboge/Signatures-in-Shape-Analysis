# Signatures in Shape analysis: An Efficient Approach to Motion Identification

## Notice: fork for Python 3

**Fork of [paalel/Signatures-in-Shape-Analysis](https://github.com/paalel/Signatures-in-Shape-Analysis).**
This fork exists to get the original codebase running on a modern Python
(verified on 3.14) and to reproduce the paper's Figure 1 on real CMU
motion-capture data. It had not been run since 2019, and two bugs crashed it
immediately on Python 3:

- `so3/dynamic_distance.py`: `xrange` &rarr; `range` (removed in Python 3)
- `so3/helpers.py` / `so3/transformations.py`: `is_3x3_matrix()` was called
  and imported but never defined anywhere — added it back

A more important bug was in `so3/clustering/signature.py`. Its `similarity()`
function had several stacked `return` statements, of which only the first
ever executes in Python — so it was silently computing `concatenate_metric`
instead of the paper's actual signature distance, `d_sig`, producing a
plausible-looking but wrong result. This is now fixed to call
`log_signature.normalized_linear_distance`, matching Figure 1 in the paper.

`so3/clustering/id_set.py` was updated to reference a freshly built database
(CMU mocap subject 16 — walk, run/jog, and forward jump). A new standalone
script, `so3/clustering/plot_dsig.py`, reproduces Figure 1's clustering
directly, without depending on the slow SRVT + dynamic-programming baseline
the database layer otherwise requires (`so3/clustering/similarity.py` still
works, but takes on the order of hours for a full pairwise run — this is the
cost the paper's signature method is contrasting itself against).

Verified against real CMU motion-capture data (18 animations, 3 classes):
clean cluster separation, computed in ~6 seconds — versus roughly 11 minutes
per pair for the paper's dynamic-programming baseline on the same machine.

# Project structure

## Animation

The animation folder contains two subfolders: src and db. 

```src/``` contains all things animation related, that is Skeleton and Animation objects,
methods for parsing .asf/.amc-files, methods for creating animations and some
attempts at different frame interpolation.

```db/``` contains data and our database. To create the tables run:

```sqlite3 <Name_of_db>.db < create_tables_sqlite3.sql```


Download the mocap data you need from http://mocap.cs.cmu.edu (per-subject
`.asf`/`.amc` files, e.g. `subjects/16/16.asf`, `subjects/16/16_05.amc`, ...) into
`db/subjects/<subject_number>/`.


create config-file: ```cp db_config_example.py db_config.py```

and add the paths to your database and subject folder.

run:

``` python insert_data_db_sqlite3.py```

to add data to database and download subject descriptions from mocap.cs.cmu.edu

```animation_manager.py``` is an interface for fetching animations in
applications

## so3

The folder so3/ contains implementation our mathematical framework for SO3.

```convert.py``` : convert animation to curce in SO3.

```transformations.py``` log, exp, interpolate, SRVT and other transformations
applied to SO3 or curves in SO3.

```curves.py```: operations that take a curve, or multiple curves as
parameters. This includes distance, dynamic_distance, close, move_origin and
others. These are all written to be functional in style.

```dynamic_distance.py```: implementations off the the dynamic distance method
proposed by Bauer.

```signature.py and log_signature.py```: proposed metrics, calculated for
geodesic interpolation curves using the iisignature library.


the folders ```experiments/``` and ```clustering/``` contain different
applications of these methods.

```clustering/similarity.py``` computes the SRVT-only and SRVT+DP baseline
distances (Figures 2 and 3 in the paper) for a set of animations defined in
```clustering/id_set.py```, and writes them to the database. It's slow — expect
on the order of minutes per pair.

```clustering/signature.py``` computes the signature-based distance (Figure 1)
for the same animations, but only writes to the database if
```similarity.py``` has already run for that pair (its writes are
update-only). If you just want Figure 1's result, use
```clustering/plot_dsig.py``` instead — a standalone script that computes the
signature distances directly and plots the MDS clustering, with no database
dependency and no need to run the slow baseline first.

## se3

Transformations applied to the group SE(3), the above mentioned framework could
be applied to this group using a similar approach.


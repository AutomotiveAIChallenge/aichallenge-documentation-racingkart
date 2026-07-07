/*
 * トップページ 動画回転プレビュー（自動回転カバーフロー）
 * - 放置で自動回転、マウス/フォーカスで停止、矢印・ドット・クリック・左右キーで選択
 * - 中央カードのクリックで lazy に iframe を読み込み再生
 * - 複数設置に対応。<div class="video-carousel" data-videos="current"> のように
 *   data-videos でセットを指定する。
 * 動画リストはこのファイル1箇所で管理する（id を null にするとプレースホルダになる）。
 */
(function () {
  "use strict";

  // 表示する動画セット（日英同一）。id が null のものはプレースホルダ。
  // セットごとに独立して編集できるよう、あえて別々の配列で定義している。
  const SETS = {
    current: [
      { id: "K_ToeWGitbk", ja: "解説① 導入編", en: "Guide 01: Introduction" },
      {
        id: "5BowSyA8hV8",
        ja: "解説② Autoware解説編",
        en: "Guide 02: Autoware",
      },
      {
        id: "MabDMP6f-Ek",
        ja: "講演① End to End AI部門の創設（TIER IV）",
        en: "Talk 1: Launch of the End-to-End AI Category (TIER IV)",
      },
      {
        id: "cGJK4Zlm11c",
        ja: "講演② コミュニティ発AIチャットボット（TPAC）",
        en: "Talk 2: Community-born AI Chatbot (TPAC)",
      },
      {
        id: "fGzGK3MC1Gw",
        ja: "講演③ 自動運転AIチャレンジの侘び寂び（SUBARU）",
        en: "Talk 3: The Wabi-Sabi of the AI Challenge (SUBARU)",
      },
      {
        id: "jrDxfqbDJd4",
        ja: "講演④ 自動運転を支えるGNSS技術（ニコン・トリンブル）",
        en: "Talk 4: GNSS for Autonomous Driving (Nikon-Trimble)",
      },
      {
        id: "Sh-8HNGfQaw",
        ja: "講演⑤ 社会実装への誘い（産総研）",
        en: "Talk 5: Toward Social Implementation (AIST)",
      },
      {
        id: "4YcWzPdrdbE",
        ja: "講演⑥ V2Xが支える協調型自動運転（東大 塚田研）",
        en: "Talk 6: Cooperative Driving with V2X (UTokyo Tsukada Lab)",
      },
      {
        id: "nG4jIycigBo",
        ja: "講演⑦ ロボット屋が見た自動運転レース世界（GMO）",
        en: "Talk 7: The World of Autonomous Racing (GMO)",
      },
    ],
    past: [
      {
        id: "z3pqjLJnENo",
        ja: "2025 予選表彰式 ダイジェスト",
        en: "2025 Preliminary Award Ceremony Digest",
      },
      {
        id: "G07HQNn1_tU",
        ja: "2025 決勝 ダイジェスト",
        en: "2025 Final Digest",
      },
      { id: "_wvVNh3_Axo", ja: "2025 決勝（2日目）", en: "2025 Final (Day 2)" },
      {
        id: "yjgMUAnJHKw",
        ja: "2025 AI vs レーサー ダイジェスト",
        en: "2025 AI vs Racer Digest",
      },
      {
        id: "Mynxk4GBAzA",
        ja: "2025 シミュレーション映像",
        en: "2025 Simulation Footage",
      },
      {
        id: "COZDHMm4E_8",
        ja: "2024 競技用EVカート 試走映像",
        en: "2024 EV Kart Test Run",
      },
      {
        id: "FGGTUcfV7nU",
        ja: "2024 ドキュメンタリー",
        en: "2024 Documentary",
      },
    ],
  };

  const AUTOPLAY_MS = 3400;
  const VISIBLE = 3; // 中央から左右に何枚まで表示するか
  // カード幅に対する横間隔・奥行きの比率（CSS のカードサイズから実測して掛ける）。
  const STEP_RATIO = 0.5;
  const DEPTH_RATIO = 0.44;

  function isEnglish() {
    const lang = (document.documentElement.lang || "").toLowerCase();
    if (lang.startsWith("en")) return true;
    if (lang.startsWith("ja")) return false;
    // フォールバック: URL パスで判定（mkdocs i18n は /en/ 配下）
    return /\/en\//.test(location.pathname);
  }

  function title(v, en) {
    return en ? v.en || v.ja : v.ja;
  }

  // 生成済みインスタンスの後始末（タイマー・リスナー）。Material の instant
  // navigation で document$ が再発火するたび、前ページ分をここで破棄する。
  let instances = [];

  function initCarousel(root) {
    if (!root || root.dataset.initialized === "true") return null;
    const videos = SETS[root.dataset.videos] || SETS.current;
    if (!videos || !videos.length) return null;
    root.dataset.initialized = "true";

    const en = isEnglish();
    const labelComingSoon = en ? "Coming soon" : "準備中";
    const n = videos.length;
    let active = 0;
    let timer = null;
    let playingIndex = null; // 再生中カードの index（未再生なら null）

    root.innerHTML = "";

    // ステージ（トラック＋矢印）
    const stage = document.createElement("div");
    stage.className = "vc-stage";

    const btnPrev = document.createElement("button");
    btnPrev.type = "button";
    btnPrev.className = "vc-btn vc-prev";
    btnPrev.setAttribute("aria-label", en ? "Previous video" : "前の動画");
    btnPrev.textContent = "‹";

    const btnNext = document.createElement("button");
    btnNext.type = "button";
    btnNext.className = "vc-btn vc-next";
    btnNext.setAttribute("aria-label", en ? "Next video" : "次の動画");
    btnNext.textContent = "›";

    const track = document.createElement("div");
    track.className = "vc-track";

    stage.appendChild(btnPrev);
    stage.appendChild(track);
    stage.appendChild(btnNext);

    const caption = document.createElement("div");
    caption.className = "vc-caption";

    const dots = document.createElement("div");
    dots.className = "vc-dots";

    root.appendChild(stage);
    root.appendChild(caption);
    root.appendChild(dots);

    const items = [];
    const dotEls = [];

    // カードをサムネイル（またはプレースホルダ）状態で描画する。
    // 初期表示と、再生停止時にプレイヤーから元へ戻す際の両方で使う。
    function fillCard(el, v) {
      el.classList.remove("vc-playing", "vc-placeholder", "vc-thumb-failed");
      el.innerHTML = "";
      if (v.id) {
        const img = document.createElement("img");
        img.className = "vc-thumb";
        img.loading = "lazy";
        img.alt = title(v, en);
        img.src = `https://img.youtube.com/vi/${v.id}/hqdefault.jpg`;
        img.addEventListener("error", function () {
          el.classList.add("vc-thumb-failed");
        });
        el.appendChild(img);

        const play = document.createElement("span");
        play.className = "vc-play";
        el.appendChild(play);

        const capIn = document.createElement("div");
        capIn.className = "vc-cap-in";
        capIn.textContent = title(v, en);
        el.appendChild(capIn);
      } else {
        el.classList.add("vc-placeholder");
        el.innerHTML =
          '<div class="vc-ph">' +
          '<span class="vc-ph-tag">' +
          labelComingSoon +
          "</span>" +
          '<span class="vc-ph-title"></span>' +
          "</div>";
        el.querySelector(".vc-ph-title").textContent = title(v, en);
      }
    }

    videos.forEach((v, i) => {
      const el = document.createElement("div");
      el.className = "vc-item";
      el.setAttribute("role", "button");
      el.setAttribute("tabindex", "-1");
      el.setAttribute("aria-label", title(v, en));
      fillCard(el, v);

      el.addEventListener("click", function () {
        if (i === active) {
          playActive();
        } else {
          setActive(i);
        }
      });

      track.appendChild(el);
      items.push(el);

      const d = document.createElement("button");
      d.type = "button";
      d.className = "vc-dot";
      d.setAttribute("aria-label", title(v, en));
      d.addEventListener("click", function () {
        setActive(i);
      });
      dots.appendChild(d);
      dotEls.push(d);
    });

    // カード間隔・奥行きは実際のカード幅から算出（CSS のカードサイズに追従）。
    function metrics() {
      const w = (items[0] && items[0].offsetWidth) || 460;
      return { step: w * STEP_RATIO, depth: w * DEPTH_RATIO };
    }

    function layout() {
      const m = metrics();
      items.forEach((el, i) => {
        let off = i - active;
        if (off > n / 2) off -= n;
        if (off < -n / 2) off += n;
        const abs = Math.abs(off);

        if (abs > VISIBLE) {
          el.style.opacity = "0";
          el.style.pointerEvents = "none";
          el.setAttribute("aria-hidden", "true");
        } else {
          el.style.opacity = "1";
          el.style.pointerEvents = "auto";
          el.removeAttribute("aria-hidden");
        }

        const x = off * m.step;
        const z = -abs * m.depth;
        const ry = off * -20;
        const scale = off === 0 ? 1 : 0.86;
        el.style.transform = `translateX(${x}px) translateZ(${z}px) rotateY(${ry}deg) scale(${scale})`;
        el.style.zIndex = String(100 - abs);
        el.classList.toggle("vc-active", off === 0);
        el.setAttribute("tabindex", off === 0 ? "0" : "-1");
      });

      dotEls.forEach((d, i) => d.classList.toggle("vc-on", i === active));
      caption.textContent = title(videos[active], en);
    }

    function setActive(i) {
      // スライドを変える前に再生中の動画を止める（音声の重なり防止）
      stopPlaying();
      active = ((i % n) + n) % n;
      layout();
    }

    // 再生中カードをサムネイルへ戻して停止し、自動回転を再開する
    function stopPlaying() {
      if (playingIndex === null) return;
      const i = playingIndex;
      playingIndex = null;
      fillCard(items[i], videos[i]);
      startAuto();
    }

    // 中央カードを実プレイヤーに差し替えて再生（プレースホルダは何もしない）
    function playActive() {
      const v = videos[active];
      if (!v.id) return;
      const el = items[active];
      if (el.querySelector("iframe")) return;

      stopAuto();
      el.classList.add("vc-playing");
      // 表示サイズは .vc-item.vc-playing iframe の CSS が担う。
      const iframe = document.createElement("iframe");
      iframe.src = `https://www.youtube-nocookie.com/embed/${v.id}?autoplay=1&rel=0`;
      iframe.title = title(v, en);
      iframe.allow =
        "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
      iframe.referrerPolicy = "strict-origin-when-cross-origin";
      iframe.allowFullscreen = true;
      el.innerHTML = "";
      el.appendChild(iframe);
      playingIndex = active;
    }

    function startAuto() {
      if (timer) return;
      // 再生中は自動回転を再開しない（動画が勝手に切り替わらないように）
      if (playingIndex !== null) return;
      if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
      timer = window.setInterval(function () {
        setActive(active + 1);
      }, AUTOPLAY_MS);
    }

    function stopAuto() {
      if (timer) {
        window.clearInterval(timer);
        timer = null;
      }
    }

    btnPrev.addEventListener("click", function () {
      setActive(active - 1);
    });
    btnNext.addEventListener("click", function () {
      setActive(active + 1);
    });

    // ホバー/フォーカスで自動回転を一時停止
    stage.addEventListener("mouseenter", stopAuto);
    stage.addEventListener("mouseleave", startAuto);
    root.addEventListener("focusin", stopAuto);
    root.addEventListener("focusout", startAuto);

    // 左右キーで選択
    root.addEventListener("keydown", function (e) {
      if (e.key === "ArrowLeft") {
        setActive(active - 1);
        e.preventDefault();
      } else if (e.key === "ArrowRight") {
        setActive(active + 1);
        e.preventDefault();
      } else if (e.key === "Enter" || e.key === " ") {
        if (
          document.activeElement &&
          document.activeElement.classList.contains("vc-item")
        ) {
          playActive();
          e.preventDefault();
        }
      }
    });

    // 画面幅変更でカード間隔を再計算（インスタンス破棄時に解除する）
    let resizeTimer = null;
    const onResize = function () {
      if (resizeTimer) window.clearTimeout(resizeTimer);
      resizeTimer = window.setTimeout(layout, 150);
    };
    window.addEventListener("resize", onResize);

    layout();
    startAuto();

    // 後始末: タイマー停止とグローバルリスナー解除
    return function cleanup() {
      stopAuto();
      if (resizeTimer) window.clearTimeout(resizeTimer);
      window.removeEventListener("resize", onResize);
    };
  }

  function boot() {
    // 前ページ分のインスタンスを破棄してから初期化（instant navigation 対策）
    instances.forEach(function (fn) {
      fn();
    });
    instances = [];
    document
      .querySelectorAll(".video-carousel[data-videos]")
      .forEach(function (root) {
        const cleanup = initCarousel(root);
        if (cleanup) instances.push(cleanup);
      });
  }

  // Material の instant navigation 対応。document$ があれば購読、無ければ通常の初期化。
  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(boot);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();

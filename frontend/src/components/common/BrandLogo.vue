<template>
  <div class="brand-logo" aria-label="메디스캔노트">
    <span class="brand-logo__mark" aria-hidden="true">
      <span></span>
      <span></span>
    </span>
    <span class="brand-logo__text">메디스캔노트</span>
  </div>
</template>

<style scoped>
.brand-logo {
  display: inline-flex;
  align-items: center;
  gap: 13px;
  color: #f6f8fb;
  font-size: 20px;
  font-weight: 800;
  letter-spacing: -0.04em;
}

.brand-logo__mark {
  position: relative;
  width: 34px;
  height: 30px;
}

.brand-logo__mark span {
  position: absolute;
  width: 21px;
  height: 21px;
  border: 2px solid var(--accent);
}

.brand-logo__mark span:first-child {
  left: 0;
  top: 0;
}

.brand-logo__mark span:last-child {
  right: 0;
  bottom: 0;
}

@media (max-width: 640px) {
  .brand-logo {
    gap: 9px;
    font-size: 17px;
  }

  .brand-logo__mark {
    width: 29px;
    height: 26px;
  }

  .brand-logo__mark span {
    width: 18px;
    height: 18px;
  }
}
</style>
